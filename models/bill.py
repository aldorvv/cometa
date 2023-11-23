from typing import List

from pydantic import BaseModel

from models.order import Order


class Bill(BaseModel):
    orders: List[Order] = []
    is_paid: bool = False
    total: int = 0
    paid: int = 0
    id: int = 0
