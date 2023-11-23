from models.order import Friends

from pydantic import BaseModel


class Payment(BaseModel):
    amount: int = 0
    customer: Friends