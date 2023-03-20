import requests
import logging
from .models import Expense

BASE_URL = "https://i1fkmq0q73.execute-api.us-east-1.amazonaws.com/test/"

def GET_expenses() -> list[Expense]:
    url = f"{BASE_URL}expenses"
    payload = {
        "operation": "GET",
        "payload": {
            "IndexName": "user-index",
            "KeyConditionExpression": "#username = :user",
            "ExpressionAttributeValues": {
                ":user": "mock_user"
            },
            "ExpressionAttributeNames": {
                "#username": "user"
            }
        }
    }
    response = requests.post(url, json=payload)
    logging.info("Obteniendo Expenses...")
    logging.info(response)
    logging.info(response.json())
    logging.info(response.status_code)
    logging.info(response.json().get('items'))

    if response.status_code == 200:
        # return response json() as Expense array
        expenses = [Expense(id=e["id"], value=e["value"], user=e["user"], description=e["description"],
                            category=e["category"], photo=e["photo"]) for e in response.json().get('items')]
        logging.info(expenses)
        logging.info(expenses[0].user)
        return expenses
    else:
        return []

def POST_expense(expense: Expense):
    url = f"{BASE_URL}expenses"
    payload = {
        "operation": "POST",
        "payload": {
            "Item": {
                "id":  expense.id,
                "value": expense.value,
                "user": expense.user,
                "description": expense.description,
                "category": expense.category,
                "photo": expense.photo,
            }
        }
    }
    logging.info(payload)
    response = requests.post(url, json=payload) 

    if response: 
        return response
    return ''