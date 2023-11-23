from http import HTTPStatus
from typing import List

import repo
from fastapi import FastAPI, HTTPException, Response
from models import Bill, Order, Payment


from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/menu")
async def get_menu():
    return repo.get_beers()


@app.get("/menu/{beer_id}")
async def get_beer(beer_id: int):
    beer = repo.get_beer(beer_id)
    if beer is not None:
        return beer
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Beer not found 🍺")


@app.post("/bills/")
async def create_bill(orders: List[Order]):
    bill = Bill()

    for order in orders:
        beer = repo.get_beer(order.beer)
        if beer is None:
            continue
        if order.quantity > beer.stock:
            order.quantity = beer.stock
        if order.quantity == 0:
            continue
        beer.stock -= order.quantity
        order.subtotal = order.quantity * beer.price
        bill.orders.append(order)

    bill.total = sum(order.subtotal for order in bill.orders)
    repo.insert_bill(bill)
    return bill


@app.get("/bills/")
async def get_bills():
    return repo.BILLS


@app.get("/bills/{bill_id}")
async def get_bill(bill_id: int):
    bill = repo.get_bill(bill_id)
    if bill is not None:
        return bill
    raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Bill not found 🧾")


@app.get("/bills/{bill_id}/total")
async def get_bill_total(bill_id: int):
    return {"total": repo.get_total(bill_id)}


@app.get("/bills/{bill_id}/debts")
async def get_debts(bill_id: int, split: bool = True):
    bill = repo.get_bill(bill_id)

    if bill is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Bill not found 🧾")
    
    if split:
        return repo.split_bill(bill_id)
    return repo.go_dutch(bill_id)


@app.patch("/bills/{bill_id}/pay")
async def pay_debt(bill_id: int, payments: List[Payment], split: bool = True):
    bill = repo.get_bill(bill_id)

    if bill is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Bill not found 🧾")
    if bill.is_paid:
        return Response(f"Bill {bill.id} is fully paid!")
    
    if split:
        debts = repo.split_bill(bill_id)
    else:
        debts = repo.go_dutch(bill_id)

    for payment in payments:
        min_amount = debts[payment.customer]
        if payment.amount < min_amount:
            raise HTTPException(status_code=HTTPStatus.PAYMENT_REQUIRED, detail=f"{payment.customer.value} owes {min_amount}")
        bill.paid += payment.amount

    if bill.paid >= bill.total:
        bill.is_paid = True
    return Response(f"Bill {bill.id} is fully paid!")

