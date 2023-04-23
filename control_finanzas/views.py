import logging
import os
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render

from control_finanzas.models import Expense, Goal, Reminder, Account
from .api import POST_goal, GET_goals, GET_expenses, POST_expense, GET_reminders, POST_reminder

from itertools import groupby
from operator import itemgetter
from datetime import datetime, timedelta
from collections import defaultdict
from PIL import Image
from io import BytesIO
from django.core.files.images import ImageFile
from django.core.files import File
from django.core.files.storage import default_storage
from django.conf import settings
import json
import matplotlib.pyplot as plt
def process_image(image):
    try:
        logging.info(f"Procesando imagen {image}")
        size = (800, 800)
        img = Image.open(image).convert('RGB')
        # Corregir la orientación de la imagen utilizando la información EXIF
        if hasattr(img, "_getexif") and img._getexif() is not None:
            exif = img._getexif()
            orientation = exif.get(0x0112, 1)  # 0x0112 es la etiqueta EXIF para orientación

            # Aplicar la transformación según la orientación
            if orientation == 2:
                img = img.transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 3:
                img = img.rotate(180)
            elif orientation == 4:
                img = img.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 5:
                img = img.rotate(-90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 6:
                img = img.rotate(-90, expand=True)
            elif orientation == 7:
                img = img.rotate(90, expand=True).transpose(Image.FLIP_LEFT_RIGHT)
            elif orientation == 8:
                img = img.rotate(90, expand=True)        
        img.thumbnail(size)
        img_io = BytesIO()
        img.save(img_io, format='JPEG', quality=70)
        img_io.seek(0)
        logging.info(f"Imagen procesada {img_io}")
        return img_io
    except Exception as e:
        logging.error(f"Error al procesar la imagen: {e}")
        raise e



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
        # Agrupar gastos por categoría
        expenses_by_category = defaultdict(list)
        for expense in expenses:
            expenses_by_category[expense.category].append(expense)

        # Calcular el ranking de los 3 mayores gastos por categoría
        for category, category_expenses in expenses_by_category.items():
            top_expenses = sorted(category_expenses, key=lambda x: float(x.value), reverse=True)[:3]
            rankings.append((category, top_expenses))

        # Calcular el total de gastos de los últimos 12 meses por categoría
        expenses_last_12_months_by_category = defaultdict(int)
        today = datetime.today()
        last_12_months = today - timedelta(days=365)
        for expense in expenses:
            if datetime.strptime(expense.date, '%Y-%m-%d') >= last_12_months:
                expenses_last_12_months_by_category[expense.category] += int(expense.value)

        # Calcular el mes con el mayor gasto total en los últimos 12 meses por categoría
        expenses_last_12_months_by_category_month = defaultdict(lambda: defaultdict(int))
        for expense in expenses:
            expense_date = datetime.strptime(expense.date, '%Y-%m-%d')
            if expense_date >= last_12_months:
                month_year = expense_date.strftime('%m-%Y')
                expenses_last_12_months_by_category_month[expense.category][month_year] += int(expense.value)

        max_month_by_category = {}
        for category, month_totals in expenses_last_12_months_by_category_month.items():
            max_month = None
            max_month_total = 0
            for month, total in month_totals.items():
                if total > max_month_total:
                    max_month_total = total
                    max_month = month
            max_month_by_category[category] = max_month

        # Calcular el día con el mayor gasto total en los últimos 12 meses por categoría
        expenses_last_12_months_by_category_day = defaultdict(lambda: defaultdict(int))
        for expense in expenses:
            expense_date = datetime.strptime(expense.date, '%Y-%m-%d')
            if expense_date >= last_12_months:
                day = expense_date.strftime('%d-%m-%Y')
                expenses_last_12_months_by_category_day[expense.category][day] += int(expense.value)

        max_day_by_category = {}
        for category, day_totals in expenses_last_12_months_by_category_day.items():
            max_day = None
            max_day_total = 0
            for day, total in day_totals.items():
                if total > max_day_total:
                    max_day_total = total
                    max_day = day
            max_day_by_category[category] = max_day


        # Obtener los datos de gastos por categoría
        expenses_by_category_graph = dict(expenses_last_12_months_by_category)
        categories_graph = list(expenses_by_category_graph.keys())
        expenses_graph = list(expenses_by_category_graph.values())

        # Crear un gráfico de torta
        fig, ax = plt.subplots()
        ax.pie(expenses_graph, labels=categories_graph, autopct='%1.1f%%')
        ax.set_title('Gastos por categoría')
        fig.set_size_inches(2, 2)
        expenses_by_category_json = json.dumps(expenses_by_category_graph)


        mensaje = "Transacción creada con éxito."
    else:
        mensaje = "Error al crear la transacción."

    return render(request, 'control_finanzas/analisis-gastos.html', {
        'mensaje': mensaje,
        "expenses": expenses,
        "rankings": rankings,
        'expenses_by_category': dict(expenses_last_12_months_by_category),
        'max_month_by_category': max_month_by_category,
        'max_day_by_category': max_day_by_category,
        'expenses_by_category_json': expenses_by_category_json
    })

@csrf_exempt
def create_expense(request):
    logging.info("Creando gasto...")
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('photo', None)
        logging.info(f'Imagen: {image}')

        try:
            if image:
              # Crea el directorio 'media' si no existe
                if not os.path.exists(settings.MEDIA_ROOT):
                  os.makedirs(settings.MEDIA_ROOT)
                
                processed_image = process_image(image)
                logging.info(f"IMAGE _ Imagen procesada: {processed_image}")
                image_name = f'image_{int(time.time() * 1000)}.jpg'
                logging.info(f"IMAGE _ Nombre de la imagen: {image_name}")
                # Guarda la imagen en el servidor local Django
                image_path = f'{settings.MEDIA_ROOT}/{image_name}'
                logging.info(f"IMAGE _ Ruta de la imagen: {image_path}")
                with open(image_path, 'wb') as f:
                  logging.info(f"IMAGE _ Guardando imagen en {image_path}")
                  f.write(processed_image.getvalue())
                  logging.info(f"IMAGE _ Imagen guardada en {image_path}")
                
                # Guarda la URL de la imagen en la variable image_url
                image_url = f'{settings.MEDIA_URL}{image_name}'
                logging.info(f"IMAGE _ URL de la imagen: {image_url}")
            else:
                image_url = "https://esteventorr.github.io/images/graphical/no-image.png"
        except Exception as e:
            logging.error(f"Error al procesar la imagen: {e}")
            image_url = "https://esteventorr.github.io/images/graphical/no-image.png"

        expense = Expense(
            value=data["value"],
            description=data["description"],
            category=data["category"],
            photo=image_url,
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
            enable_target_date=data.get(
                "enable_target_date", "false").lower() == 'on',
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
    # Valor establecido para declarar renta (ejemplo)
    valor_declaracion = 163445400
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
