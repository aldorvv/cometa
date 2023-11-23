from pydantic import BaseModel
from enum import Enum


class BeerType(str, Enum):
    LAGER = "Lager"
    IPA = "IPA"
    PALE_ALE = "Pale Ale"
    STOUT = "Stout"


class Beer(BaseModel):
    id: int
    name: str
    type_: BeerType
    price: int
    stock: int
