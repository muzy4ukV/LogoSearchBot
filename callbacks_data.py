from typing import Optional
from aiogram.filters.callback_data import CallbackData


class ShowLabelData(CallbackData, prefix='label'):
    action: str
    value: Optional[bool] = None