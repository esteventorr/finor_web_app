import requests

postObject = {
    "operation": "create",
    "payload": {
        "Item": {
            "id": "expense_",
            "number": 0,
            "user": "mock_user"
        }
    }
}

readObject = {
    "operation": "read",
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

endpointAWS = '';


def generate_post_request(url, params={}):
    response = requests.post(url, json=params)

    if response.status_code == 200:
        return response.json()


def get_expenses():

    response = generate_post_request(
        endpointAWS, readObject)
    if response:
        # user = response.get('results')[0]
        return response  # user.get('name').get('first')

    return ''

def save_expense(value, description, categoty, image):
    localPostObject = {
    "operation": "create",
    "payload": {
        "Item": {
            "id": "expense_",
            "value": value,
            "user": "mock_user",
            "description": description,
            "category": categoty,
            "photo": image,
        }
    }
}
    response = generate_post_request(
        endpointAWS, localPostObject)
    if response:
        # user = response.get('results')[0]
        return response  # user.get('name').get('first')

    return ''
