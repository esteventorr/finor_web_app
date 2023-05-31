import logging
import os
import time
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render

from dateutil.relativedelta import relativedelta
from control_finanzas.models import Expense, Goal, Reminder, Account
from control_finanzas.templatetags.custom_filters import currency
from helpers.auth import require_auth
from .api import (
    POST_accounts,
    POST_goal,
    GET_goals,
    GET_expenses,
    POST_expense,
    GET_reminders,
    POST_reminder,
)

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
from firebase_admin import auth
from django.core.management.utils import get_random_secret_key  


def logout(request):
    request.user = None
    return JsonResponse({"message": "Desconexión exitosa"})

def process_image(image):
    try:
        logging.info(f"Procesando imagen {image}")
        size = (800, 800)
        img = Image.open(image).convert("RGB")
        # Corregir la orientación de la imagen utilizando la información EXIF
        if hasattr(img, "_getexif") and img._getexif() is not None:
            exif = img._getexif()
            orientation = exif.get(
                0x0112, 1
            )  # 0x0112 es la etiqueta EXIF para orientación

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
        img.save(img_io, format="JPEG", quality=70)
        img_io.seek(0)
        logging.info(f"Imagen procesada {img_io}")
        return img_io
    except Exception as e:
        logging.error(f"Error al procesar la imagen: {e}")
        raise e

def get_total_by_category(expenses):
    totals = defaultdict(int)
    for expense in expenses:
        totals[expense.category] += float(expense.value)
    return totals

@require_auth
def main_menu(request):
    print(get_random_secret_key())
    user_display_name = request.session['user_display_name']
    return render(request, "control_finanzas/main-menu.html", {"user_display_name": user_display_name})

def under_development(request):
    return render(request, "control_finanzas/under-development.html", {})

def login_page(request):
    return render(request, "control_finanzas/login-page.html", {})

def signup_page(request):
    return render(request, "control_finanzas/signup-page.html", {})

@require_auth
def ingresar_gastos(request):
    logging.info("Ingresando gastos...")
    expenses = GET_expenses(request)
    if expenses:
        mensaje = "Transacción creada con éxito."
    else:
        mensaje = "Error al crear la transacción."
    logging.info(mensaje)
    return render(
        request,
        "control_finanzas/crear-gastos.html",
        {"mensaje": mensaje, "expenses": expenses},
    )

@require_auth
def ingresar_objetivos(request):
    logging.info("Ingresando objetivos...")
    unfiltered_expenses = GET_expenses(request)
    expenses = [expense for expense in unfiltered_expenses if expense.category == "goalabono"]
    goals = GET_goals(request)
    if goals:
        mensaje = "Objetivo creado con éxito."
    else:
        mensaje = "Error al crear el objetivo."
    logging.info(mensaje)
    for goal in goals:
        goal.total_expenses = sum(int(expense.value) for expense in expenses if expense.description == goal.id)
    return render(
        request,
        "control_finanzas/crear-objetivos.html",
        {"mensaje": mensaje, "goals": goals, "expenses": expenses},
    )

@require_auth
def abonar_objetivo(request):
    logging.info("Abonando objetivo...")
    if request.method == "POST":
        data = request.POST
        
        expense = Expense(
            value=data["value"],
            description="{{}}",
            category="goalabono",
            user=request.session['user_display_name'],
        )

        response = POST_expense(expense)
        response_data = response.json()
        logging.info(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})

@require_auth
def ingresar_recordatorios(request):
    logging.info("Ingresando recordatorios...")
    reminders = GET_reminders(request)
    if reminders:
        mensaje = "Objetivo creado con éxito."
    else:
        mensaje = "Error al crear el objetivo."
    logging.info(mensaje)
    return render(
        request,
        "control_finanzas/crear-recordatorios.html",
        {"mensaje": mensaje, "reminders": reminders},
    )

@require_auth
def analisis_gastos(request):
    user_display_name = request.session['user_display_name']
    user_uid = request.session['user_uid']
    logging.info(f"Usuario autenticado: {user_display_name} {user_uid}")
    unfiltered_expenses = GET_expenses(request)
    expenses = [expense for expense in unfiltered_expenses if expense.category != "goalabono"]
    rankings = []
    if expenses:
        # Agrupar gastos por categoría
        expenses_by_category = defaultdict(list)
        for expense in expenses:
            expenses_by_category[expense.category].append(expense)

        # Calcular el ranking de los 3 mayores gastos por categoría
        for category, category_expenses in expenses_by_category.items():
            top_expenses = sorted(
                category_expenses, key=lambda x: float(x.value), reverse=True
            )[:3]
            rankings.append((category, top_expenses))

        # Calcular el total de gastos de los últimos 12 meses por categoría
        expenses_last_12_months_by_category = defaultdict(int)
        today = datetime.today()
        last_12_months = today - timedelta(days=365)
        for expense in expenses:
            if datetime.strptime(expense.date, "%Y-%m-%d") >= last_12_months:
                expenses_last_12_months_by_category[expense.category] += int(
                    expense.value
                )

        # Calcular el mes con el mayor gasto total en los últimos 12 meses por categoría
        expenses_last_12_months_by_category_month = defaultdict(
            lambda: defaultdict(int)
        )
        for expense in expenses:
            expense_date = datetime.strptime(expense.date, "%Y-%m-%d")
            if expense_date >= last_12_months:
                month_year = expense_date.strftime("%m-%Y")
                expenses_last_12_months_by_category_month[expense.category][
                    month_year
                ] += int(expense.value)

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
            expense_date = datetime.strptime(expense.date, "%Y-%m-%d")
            if expense_date >= last_12_months:
                day = expense_date.strftime("%d-%m-%Y")
                expenses_last_12_months_by_category_day[expense.category][day] += int(
                    expense.value
                )

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
        ax.pie(expenses_graph, labels=categories_graph, autopct="%1.1f%%")
        ax.set_title("Gastos por categoría")
        fig.set_size_inches(2, 2)
        expenses_by_category_json = json.dumps(expenses_by_category_graph)

        mensaje = "Transacción creada con éxito."
    else:
        mensaje = "Error al crear la transacción."

    return render(
        request,
        "control_finanzas/analisis-gastos.html",
        {
            "mensaje": mensaje,
            "expenses": expenses,
            "rankings": rankings,
            "expenses_by_category": dict(expenses_last_12_months_by_category),
            "max_month_by_category": max_month_by_category,
            "max_day_by_category": max_day_by_category,
            "expenses_by_category_json": expenses_by_category_json,
        },
    )

@csrf_exempt
def create_expense(request):
    logging.info("Creando gasto...")
    if request.method == "POST":
        data = request.POST
        image = request.FILES.get("photo", None)
        logging.info(f"Imagen: {image}")

        try:
            if image:
                # Crea el directorio 'media' si no existe
                if not os.path.exists(settings.MEDIA_ROOT):
                    os.makedirs(settings.MEDIA_ROOT)

                processed_image = process_image(image)
                logging.info(f"IMAGE _ Imagen procesada: {processed_image}")
                image_name = f"image_{int(time.time() * 1000)}.jpg"
                logging.info(f"IMAGE _ Nombre de la imagen: {image_name}")
                # Guarda la imagen en el servidor local Django
                image_path = f"{settings.MEDIA_ROOT}/{image_name}"
                logging.info(f"IMAGE _ Ruta de la imagen: {image_path}")
                with open(image_path, "wb") as f:
                    logging.info(f"IMAGE _ Guardando imagen en {image_path}")
                    f.write(processed_image.getvalue())
                    logging.info(f"IMAGE _ Imagen guardada en {image_path}")

                # Guarda la URL de la imagen en la variable image_url
                image_url = f"{settings.MEDIA_URL}{image_name}"
                logging.info(f"IMAGE _ URL de la imagen: {image_url}")
            else:
                image_url = (
                    "https://esteventorr.github.io/images/graphical/no-image.png"
                )
        except Exception as e:
            logging.error(f"Error al procesar la imagen: {e}")
            image_url = "https://esteventorr.github.io/images/graphical/no-image.png"

        expense = Expense(
            value=data["value"],
            description=data["description"],
            category=data["category"],
            photo=image_url,
            date=data["date"],
            user=request.session['user_display_name'],
        )

        response = POST_expense(expense)
        response_data = response.json()
        logging.info(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def create_goal(request):
    logging.info("Creando objetivo...")
    if request.method == "POST":
        data = request.POST
        logging.info(data)
        goal = Goal(
            enable_target_date=data.get("enable_target_date", "false").lower() == "on",
            name=data["name"],
            set_date=data["set_date"],
            target_date=data["target_date"],
            value=data["value"],
            description=data["description"],
            category=data["category"],
            user=request.session['user_display_name'],
        )
        response = POST_goal(goal)
        response_data = response.json()
        logging.info(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})
    
@csrf_exempt
def addgoalabonoexpense(request):
    if request.method == "POST":
        data = request.POST
        logging.info(data)
        try:
            image_url = "https://esteventorr.github.io/images/graphical/no-image.png"
            expense = Expense(
                value=data["value-input"],
                description=data["goal-id"],
                category="goalabono",
                photo=image_url,
                date="2000-01-01",
                user=request.session['user_display_name'],
            )
            POST_expense(
                expense
            )
            return JsonResponse({"message": "Abono generado exitosamente"})
        except Exception as e:
            logging.error(f"Error al abonar: {e}")
            return JsonResponse({"message": "Error al abonar"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def signup(request):
    if request.method == "POST":
        data = request.POST
        logging.info(data)
        try:
            user = auth.create_user(
                email=data["email"],
                email_verified=False,
                password=data["password"],
                display_name=data["username"],
                disabled=False,
            )
            logging.info(f"Usuario creado: {user}")
            POST_accounts(
                Account(
                    user=data["username"],
                    name="undefined",
                    born_date="2000-01-01",
                    first_name="undefined",
                    last_name="undefined",
                    uid=user.uid,
                )
            )
            return JsonResponse({"message": "Usuario creado exitosamente"})
        except Exception as e:
            logging.error(f"Error al crear el usuario: {e}")
            return JsonResponse({"message": "Error al crear el usuario"}, status=500)
    else:
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def login(request):
    if request.method == "POST":
        data = request.POST
        logging.info(data)
        return JsonResponse({"message": "Exito al iniciar sesión"})
    else:
        return JsonResponse({"error": "Invalid request method"})

@csrf_exempt
def create_reminder(request):
    logging.info("Creando recordatorio...")
    if request.method == "POST":
        data = request.POST
        logging.info(data)
        reminder = Reminder(
            name=data["name"],
            set_date=data["set_date"],
            target_date=data["target_date"],
            description=data["description"],
            user=request.session['user_display_name'],
        )
        response = POST_reminder(reminder)
        response_data = response.json()
        logging.info(response_data)
        return JsonResponse(response_data)
    else:
        return JsonResponse({"error": "Invalid request method"})

@require_auth
def calendario(request):
    current_month = datetime.now().month
    filtered_goals = [
        goal
        for goal in GET_goals(request)
        if datetime.strptime(goal.target_date, "%Y-%m-%d").month == current_month
    ]
    return render(request, "control_finanzas/calendar.html", {"goals": filtered_goals})

@require_auth
def mensajes_alertas(request):
    expenses = GET_expenses(request)

    # Declaración de renta
    year = datetime.now().year - 1
    total_ingresos = calcular_total_ingresos(expenses, year)
    # Valor establecido para declarar renta (ejemplo)
    valor_declaracion = 163445400
    if total_ingresos > valor_declaracion:
        mensaje = f"¡Alerta! Tus ingresos totales del año pasado fueron de {currency(total_ingresos)}, lo cual supera el valor establecido para declarar renta. Debes hacer la respectiva declaración de renta."
    else:
        mensaje = f"Tus ingresos totales del año pasado fueron de {currency(total_ingresos)}, lo cual no supera el valor establecido para declarar renta. ¡Sigues sin tener que declarar renta!"

    # Comparación de gastos con mismo día mes anterior
    today = datetime.now()
    current_month_start = today.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    last_month_start = current_month_start - relativedelta(months=1)
    last_month_end = current_month_start - relativedelta(days=1)

    current_expenses = [
        e
        for e in expenses
        if last_month_end < datetime.strptime(e.date, "%Y-%m-%d") <= today
    ]
    past_expenses = [
        e
        for e in expenses
        if last_month_start <= datetime.strptime(e.date, "%Y-%m-%d") <= last_month_end
    ]

    current_totals = get_total_by_category(current_expenses)
    past_totals = get_total_by_category(past_expenses)
    categories = set(current_totals.keys()) | set(past_totals.keys())

    logging.info(f"current_totals: {current_totals}")
    logging.info(f"past_totals: {past_totals}")

    for category in categories:
        if category not in current_totals:
            current_totals[category] = 0
        if category not in past_totals:
            past_totals[category] = 0

    # Obtener el nombre del mes actual en español
    month_names = [
        "enero",
        "febrero",
        "marzo",
        "abril",
        "mayo",
        "junio",
        "julio",
        "agosto",
        "septiembre",
        "octubre",
        "noviembre",
        "diciembre",
    ]
    current_month_name = month_names[today.month - 1]

    # Calcular las diferencias de porcentaje
    differences = {}
    for category in categories:
        current_total = current_totals.get(category, 0)
        past_total = past_totals.get(category, 0)
        if past_total == 0:
            difference = 0
        else:
            difference = (current_total - past_total) / past_total * 100
        differences[category] = difference
    logging.info(f"differences: {differences}")

    return render(
        request,
        "control_finanzas/mensajes-alertas.html",
        {
            "expenses": expenses,
            "mensaje": mensaje,
            "mes_actual": current_month_name,
            "current_totals": current_totals.items(),
            "past_totals": past_totals,
            "differences": differences,
        },
    )

def calcular_total_ingresos(expenses, year):
    total = 0
    for expense in expenses:
        date_obj = datetime.strptime(expense.date, "%Y-%m-%d").date()
        if date_obj.year == year and expense.category == "ingreso":
            # Convertir el valor a entero antes de sumarlo
            total += int(expense.value)
    return total

@csrf_exempt
def set_user(request):
    if request.method == "POST":
        user_display_name = request.POST.get("displayName")
        user_uid = request.POST.get("uid")
        if user_display_name is not None:
            # un usuario ha iniciado sesión
            request.session["user_display_name"] = user_display_name
            request.session["user_uid"] = user_uid
            return JsonResponse({"status": "success", "redirect": "/"}) # Cambia esto por la URL de tu página principal
        else:
            # no hay un usuario logueado, limpia la sesión
            if "user_display_name" in request.session:
                del request.session["user_display_name"]
            if "user_uid" in request.session:
                del request.session["user_uid"]
            return JsonResponse({"status": "failure", "redirect": "/loginpage"}) # Cambia esto por la URL de tu página de login
    else:
        return JsonResponse({"error": "Invalid request method"}, status=405)

