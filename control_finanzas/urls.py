from django.urls import path
from . import views

urlpatterns = [
    path("", views.main_menu, name="main_menu"),
    path("crear-gastos/", views.ingresar_gastos, name="crear_gastos"),
    path("create_expense/", views.create_expense, name="create_expense"),
    path("metas-ahorros/", views.ingresar_objetivos, name="metas_ahorros"),
    path("analisis-gastos/", views.analisis_gastos, name="analisis_gastos"),
    path("mensajes-alertas/", views.mensajes_alertas, name="mensajes_alertas"),
    path("create_goal/", views.create_goal, name="create_goal"),
    path("abonar_objetivo", views.addgoalabonoexpense, name="abonar_objetivo"),
    path("create_reminder/", views.create_reminder, name="create_reminder"),
    path("signup/", views.signup, name="signup"),
    path("calendario/", views.calendario, name="calendario"),
    path("login/", views.login, name="login"),
    path("loginpage/", views.login_page, name="loginpage"),
    path("signuppage/", views.signup_page, name="signuppage"),
    path("logout/", views.logout, name="logout"),
    path("setuser/", views.set_user, name="set_user"),
]
