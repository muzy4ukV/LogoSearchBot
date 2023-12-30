from database.base import Base, int64, str_40
from sqlalchemy.orm import Mapped

from typing import Optional

from sqlalchemy.orm import mapped_column


class User(Base):
    __tablename__ = 'users'

    user_id: Mapped[int64] = mapped_column(primary_key=True)
    username: Mapped[Optional[str_40]] = mapped_column(unique=True)
    sens_level: Mapped[float] = mapped_column(default=0.5)
    data_folder: Mapped[str]
    result_folder: Mapped[str]
    show_labels: Mapped[bool] = mapped_column(default=True)
    num_of_requests: Mapped[int] = mapped_column(default=0)

