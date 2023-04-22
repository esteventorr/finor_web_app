import requests
import logging
from .models import Expense, Goal, Reminder, Account

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
    #logging.info(response.json())
    #logging.info(response.status_code)
    #logging.info(response.json().get('items'))

    if response.status_code == 200:
        # return response json() as Expense array
        expenses = [Expense(id=e["id"], value=e["value"], user=e["user"], description=e["description"],
                            category=e["category"], photo=e["photo"], date=e["date"] ) for e in response.json().get('items')]
        logging.info(expenses)
        #logging.info(expenses[0].user)
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
                "date": expense.date
            }
        }
    }
    logging.info(payload)
    response = requests.post(url, json=payload)

    if response:
        return response
    return ''


def GET_goals() -> list[Goal]:
    url = f"{BASE_URL}goals"
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
    logging.info("Obteniendo Goals...")
    logging.info(response)
    logging.info(response.json())
    logging.info(response.status_code)
    logging.info(response.json().get('items'))

    if response.status_code == 200:
        # return response json() as Goal array
        goals = [Goal(
            id=g["id"], enable_target_date=g["enable_target_date"], name=g["name"], set_date=g["set_date"],
            target_date=g["target_date"], value=g["value"], user=g["user"], description=g["description"],
            category=g["category"]
        ) for g in response.json().get('items')]
        logging.info(goals)
        logging.info(goals[0].user)
        return goals
    else:
        return []


def POST_goal(goal: Goal):
    url = f"{BASE_URL}goals"
    payload = {
        "operation": "POST",
        "payload": {
            "Item": {
                "id": goal.id,
                "enable_target_date": goal.enable_target_date,
                "name": goal.name,
                "set_date": goal.set_date,
                "target_date": goal.target_date,
                "value": goal.value,
                "user": goal.user,
                "description": goal.description,
                "category": goal.category,
            }
        }
    }
    logging.info(payload)
    response = requests.post(url, json=payload)

    if response:
        return response

    return ''


def GET_reminders() -> list[Reminder]:
    url = f"{BASE_URL}reminders"
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
    logging.info("Obteniendo Reminders...")
    logging.info(response)
    logging.info(response.json())
    logging.info(response.status_code)
    logging.info(response.json().get('items'))

    if response.status_code == 200:
        # return response json() as Reminder array
        reminders = [Reminder(
            id=r["id"], name=r["name"], set_date=r["set_date"],
            target_date=r["target_date"]
        ) for r in response.json().get('items')]
        logging.info(reminders)
        logging.info(reminders[0].user)
        return reminders
    else:
        return []

def POST_reminder(reminder: Reminder):
    url = f"{BASE_URL}reminders"
    payload = {
        "operation": "POST",
        "payload": {
            "Item": {
                "id": reminder.id,
                "name": reminder.name,
                "set_date": reminder.set_date,
                "target_date": reminder.target_date,
                "user": reminder.user,
                "description": reminder.description
            }
        }
    }
    logging.info(payload)
    response = requests.post(url, json=payload)
    if response:
        return response
    return ''