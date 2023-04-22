from datetime import datetime
import logging
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from control_finanzas.models import Expense, Goal, Reminder, Account
from .api import POST_goal, GET_goals, GET_expenses, POST_expense, GET_reminders, POST_reminder

from itertools import groupby
from operator import itemgetter

def main_menu(request):
    return render(request, 'control_finanzas/main-menu.html')

def under_development(request):
    return render(request, 'control_finanzas/under-development.html', {})

def ingresar_gastos(request):
    logging.info("Ingresando gastos...")
    expenses = GET_expenses()
    if expenses:
        mensaje = "Transacción creada con éxito."
    else:
        mensaje = "Error al crear la transacción."
    logging.info(mensaje)
    return render(request, 'control_finanzas/crear-gastos.html', {'mensaje': mensaje, "expenses": expenses})

def ingresar_objetivos(request):
    logging.info("Ingresando objetivos...")
    goals = GET_goals()
    if goals:
        mensaje = "Objetivo creado con éxito."
    else:
        mensaje = "Error al crear el objetivo."
    logging.info(mensaje)
    return render(request, 'control_finanzas/crear-objetivos.html', {'mensaje': mensaje, "goals": goals})

def ingresar_recordatorios(request):
    logging.info("Ingresando recordatorios...")
    reminders = GET_reminders()
    if reminders:
        mensaje = "Objetivo creado con éxito."
    else:
        mensaje = "Error al crear el objetivo."
    logging.info(mensaje)
    return render(request, 'control_finanzas/crear-recordatorios.html', {'mensaje': mensaje, "reminders": reminders})

def analisis_gastos(request):
    expenses = GET_expenses()
    rankings = []
    if expenses:
        # Obtener los gastos agrupados por categoría
        expenses_by_category = {k: list(g) for k, g in groupby(expenses, key=lambda x: x.category)}
        # Calcular el ranking de los 3 mayores gastos por categoría
        for category, category_expenses in expenses_by_category.items():
            top_expenses = sorted(category_expenses, key=lambda x: x.value, reverse=True)[:3]
            rankings.append((category, top_expenses))
        mensaje = "Transacción creada con éxito."
    else:
        mensaje = "Error al crear la transacción."
    logging.info(mensaje)
    logging.info(f"Rankings: {rankings}")
    return render(request, 'control_finanzas/analisis-gastos.html', {'mensaje': mensaje, "expenses": expenses, "rankings": rankings})


@csrf_exempt
def create_expense(request):
    logging.info("Creando gasto...") 
    if request.method == 'POST':
        data = request.POST 
        expense = Expense( 
            value=data["value"], 
            description=data["description"],
            category=data["category"],
            photo="https://esteventorr.github.io/images/graphical/no-image.png",
            date=data["date"],
        )
        response = POST_expense(expense) 
        response_data = response.json()
        logging.info(response_data) 
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def create_goal(request):
    logging.info("Creando objetivo...")
    if request.method == 'POST':
        data = request.POST
        logging.info(data)
        goal = Goal(
            enable_target_date=data.get("enable_target_date", "false").lower() == 'on',
            name=data["name"],
            set_date=data["set_date"],
            target_date=data["target_date"],
            value=data["value"],
            description=data["description"],
            category=data["category"],
        )
        response = POST_goal(goal)
        response_data = response.json()
        logging.info(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})

@csrf_exempt
def create_reminder(request):
    logging.info("Creando recordatorio...")
    if request.method == 'POST':
        data = request.POST
        logging.info(data)
        reminder = Reminder( 
            name=data["name"],
            set_date=data["set_date"],
            target_date=data["target_date"],
            description=data["description"],
        )
        response = POST_reminder(reminder)
        response_data = response.json()
        logging.info(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({'error': 'Invalid request method'})
    
def calendario(request):
    return render(request, 'control_finanzas/calendar.html')
    
def mensajes_alertas(request):
    expenses = GET_expenses()
    year = datetime.now().year - 1
    total_ingresos = calcular_total_ingresos(expenses, year)
    valor_declaracion = 163445400  # Valor establecido para declarar renta (ejemplo)
    if total_ingresos > valor_declaracion:
        mensaje = f"¡Alerta! Tus ingresos totales del año pasado fueron de ${total_ingresos}, lo cual supera el valor establecido para declarar renta. Debes hacer la respectiva declaración de renta."
    else:
        mensaje = f"Tus ingresos totales del año pasado fueron de ${total_ingresos}, lo cual no supera el valor establecido para declarar renta. ¡Sigues sin tener que declarar renta!"

    return render(request, 'control_finanzas/mensajes-alertas.html', {"expenses": expenses, "mensaje": mensaje})

def calcular_total_ingresos(expenses, year):
    total = 0
    for expense in expenses:
        date_obj = datetime.strptime(expense.date, '%Y-%m-%d').date()
        if date_obj.year == year and expense.category == "ingreso":
            # Convertir el valor a entero antes de sumarlo
            total += int(expense.value)
    return total
