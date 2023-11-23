import math
from itertools import groupby
from typing import Dict, List, Optional
from models import Beer, BeerType, Bill, Friends


BILLS = [Bill(**{
    "orders": [
        {
            "beer": 1,
            "quantity": 1,
            "subtotal": 300,
            "customer": "Scott Pilgrim"
        },
        {
            "beer": 2,
            "quantity": 2,
            "subtotal": 700,
            "customer": "Scott Pilgrim"
        },
        {
            "beer": 4,
            "quantity": 1,
            "subtotal": 500,
            "customer": "Kim Pine"
        },
        {
            "beer": 3,
            "quantity": 2,
            "subtotal": 500,
            "customer": "Stephen Stills"
        },
        {
            "beer": 4,
            "quantity": 1,
            "subtotal": 500,
            "customer": "Stephen Stills"
        }
    ],
    "is_paid": False,
    "total": 2500,
    "paid": 0,
    "id": 1
})]

FRIENDS = (Friends.SCOTT, Friends.KIM, Friends.STEPHEN)

BEERS = [
    Beer(id=1, name="Duff Premium Lager", type_=BeerType.LAGER, price=300, stock=30),
    Beer(id=2, name="Duff India Pale Ale", type_=BeerType.IPA, price=350, stock=50),
    Beer(id=3, name="Duff Christmas Ale", type_=BeerType.PALE_ALE, price=250, stock=40),
    Beer(id=4, name="Duff Black", type_=BeerType.STOUT, price=500, stock=15),
]


def get_beers() -> List[Dict]:
    return [beer for beer in BEERS if beer.stock]


def get_beer(id_: int) -> Optional[Beer]:
    for beer in BEERS:
        if beer.id == id_:
            return beer
    return None


def insert_bill(bill: Bill):
    bill.id = len(BILLS) + 1
    BILLS.append(bill)


def get_bill(bill_id: int) -> Bill:
    for bill in BILLS:
        if bill.id == bill_id:
            return bill
    return None


def get_total(bill_id: int) -> int:
    bill = get_bill(bill_id)
    if bill is None:
        return 0
    return bill.total


def split_bill(bill_id: int) -> Dict:
    return {friend: math.ceil(get_total(bill_id) / len(FRIENDS)) for friend in FRIENDS}


def go_dutch(bill_id: int) -> Dict:
    bill = get_bill(bill_id)
    grouped = {key: list(group) for key, group in groupby(bill.orders, key=lambda x: x.customer)}
    return {friend: sum(order.subtotal for order in grouped[friend]) for friend in FRIENDS}

