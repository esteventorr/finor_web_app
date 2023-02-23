# Logging configuration
import json
from django.http import JsonResponse
from sandbox.utils import finorRestAPI
from django.http import HttpResponse
from django.shortcuts import render
import logging
import logging.config
import sys
LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO'
    }
}
logging.config.dictConfig(LOGGING)


# Create your views here.


def saved_expenses(requests):
    logging.info(requests)
    response = finorRestAPI.get_expenses()
    # response is dict
    logging.info(response)

    displayExpenses = False
    expenses = []
    if response.get('status') == 200 and response.get('count') > 0:
        displayExpenses = True
        expenses = response.get('items')

    context = {
        'name': "Mock User",
        'expenses': expenses if displayExpenses else []
    }
    logging.info(context)
    return render(requests, 'create-expense.html', context)
# Si así lo deseamos poder enviar parametros a nuestra petición.


def listExpensesView(requests):
    params = {'order': 'desc'}

    context = {
        'name': "test"  # finorRestAPI.get_expenses(params)
    }
    return render(requests, 'create-expense.html', context)


def home(request):
    return HttpResponse("Hello World")  # Could be HTML


def get_expenses(request):
    logging.info("Request Entry:")
    logging.info(request)
    # get valor url query parameter from WSGIRequest object
    value = request.GET.get('valor')
    logging.info(request.GET)
    description = request.GET.get('descripcion')
    logging.info(description)
    category = request.GET.get('categoria')
    image = request.GET.get('imagen')
    logging.info(image)
    # check if the variables are not empty
    response = ""
    if value != "" and description != "" and category != "" and image != "":
        response = finorRestAPI.save_expense(
            value, description, category, image)
    return JsonResponse(response, safe=False)
