from contextlib import contextmanager

import sqlalchemy as sa
from sqlalchemy import select, text, update
from sqlalchemy.inspection import inspect
from sqlalchemy.orm import DeclarativeBase, joinedload
from sqlalchemy.orm.session import Session

from typing import Annotated

from settings import settings

str_40 = Annotated[str, 40]
int64 = Annotated[int, 8]


class Base(DeclarativeBase):
    type_annotation_map = {
        int64: sa.BigInteger(),
        str_40: sa.String(40)
    }

    @classmethod
    def primary_key(cls):
        return inspect(cls).primary_key[0]

    def delete(self):
        with session_scope() as session:
            return session.delete(self)

    def update(self, **kwargs):
        pk = self.primary_key().name
        pk_value = getattr(self, pk)
        with session_scope() as session:
            session.execute(
                update(
                    type(self)
                ).where(
                    text(f"{pk} = '{pk_value}'")
                ).values(
                    **kwargs
                )
            )
        return type(self).get_pk(pk_value)

    @classmethod
    def get(
        cls,
        filter_statement=None,
        limit: int = 1,
        order_by=None
    ):
        statement = select(cls)
        if filter_statement is not None:
            statement = statement.where(filter_statement)

        if order_by:
            statement = statement.order_by(order_by)

        with session_scope() as session:
            if limit and limit == 1:
                return session.scalar(statement)

            return session.scalars(statement).unique().all()

    @classmethod
    def get_all(cls, filter_statement=None, order_by=None):
        return cls.get(filter_statement, order_by=order_by)

    @classmethod
    def get_pk(cls, pk_value) -> 'Base':
        pk = cls.primary_key().name
        return cls.get(getattr(cls, pk) == pk_value)

    @classmethod
    def add_new(cls, **kwargs) -> 'Base':
        new_obj = cls(**kwargs)
        with session_scope() as session:
            session.add(new_obj)
        return new_obj


engine = sa.create_engine(
    f'postgresql+psycopg2://{settings.DB_USER}:{settings.DB_PASSWORD.get_secret_value()}@' +
    f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.DB_NAME}',
    echo=False
)


@contextmanager
def session_scope() -> Session:
    session = Session(engine, expire_on_commit=False)
    try:
        yield session
        session.commit()
    except Exception as exc:
        session.rollback()
        raise exc
    finally:
        session.close()
