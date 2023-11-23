from enum import Enum
from typing import List

from pydantic import BaseModel


class Friends(str, Enum):
    SCOTT = "Scott Pilgrim"
    KIM = "Kim Pine"
    STEPHEN = "Stephen Stills"


class Order(BaseModel):
    beer: int
    quantity: int = 0
    subtotal: int = 0

    customer: Friends