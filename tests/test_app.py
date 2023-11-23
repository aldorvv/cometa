import sys
import os

from fastapi.testclient import TestClient

sys.path.append(os.getcwd())
print(sys.path)
from app import app
from models import Order, Payment

client = TestClient(app)

def test_get_menu():
    response = client.get("/menu")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_beer():
    response = client.get("/menu/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "id" in response.json()

    response = client.get("/menu/999")
    assert response.status_code == 404

def test_create_bill():
    menu_response = client.get("/menu")
    assert menu_response.status_code == 200
    menu_data = menu_response.json()
    assert menu_data
    
    order = Order(beer=menu_data[0]["id"], quantity=1, customer="Scott Pilgrim")
    response = client.post("/bills/", json=[order.model_dump()], headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "id" in response.json()

def test_get_bills():
    response = client.get("/bills/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_bill():
    bills_response = client.get("/bills/")
    assert bills_response.status_code == 200
    bills_data = bills_response.json()
    assert bills_data

    response = client.get(f"/bills/{bills_data[0]['id']}")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "id" in response.json()

def test_get_bill_total():
    bills_response = client.get("/bills/")
    assert bills_response.status_code == 200
    bills_data = bills_response.json()
    assert bills_data

    response = client.get(f"/bills/{bills_data[0]['id']}/total")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)
    assert "total" in response.json()

def test_get_debts():
    bills_response = client.get("/bills/")
    assert bills_response.status_code == 200
    bills_data = bills_response.json()
    assert bills_data

    response = client.get(f"/bills/{bills_data[0]['id']}/debts")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_pay_debt():
    bills_response = client.get("/bills/")
    assert bills_response.status_code == 200
    bills_data = bills_response.json()
    assert bills_data

    id = bills_data[0]['id']
    debts_response = client.get(f"/bills/{id}/debts")
    assert debts_response.status_code == 200
    debts_data = debts_response.json()
    assert debts_data

    payments = [Payment(customer=customer, amount=debts_data[customer]).model_dump() for customer in debts_data]
    response = client.patch(f"/bills/{id}/pay", json=payments, headers={"Content-Type": "application/json"})
    assert response.status_code == 200

    response = client.patch(f"/bills/{id}/pay", json=payments, headers={"Content-Type": "application/json"})
    assert response.status_code == 200
    assert "fully paid" in response.text
