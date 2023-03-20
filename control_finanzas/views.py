import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from control_finanzas.models import Expense
from .api import POST_expense 

def main_menu(request):
    return render(request, 'control_finanzas/main-menu.html')

@csrf_exempt
def create_expense(request):
    logging.info("Creando gasto...") 
    if request.method == 'POST':
        data = request.POST 
        expense = Expense( 
            value=data["value"], 
            description=data["description"],
            category=data["category"],
            photo="https://esteventorr.github.io/images/graphical/no-image.png"
        )
        response = POST_expense(expense) 
        response_data = response.json()
        logging.info(response_data) 
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
