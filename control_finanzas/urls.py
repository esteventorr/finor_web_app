from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('crear-gastos/', views.ingresar_gastos, name='crear_gastos'),
    path('create_expense/', views.create_expense, name='create_expense'),
    path('analisis-gastos/', views.analisis_gastos, name='analisis_gastos'),
    path('mensajes-alertas/', views.under_development, name='mensajes_alertas'),
]
