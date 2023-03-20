from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('crear-gastos/', views.ingresar_gastos, name='crear_gastos'),
    path('create_expense/', views.create_expense, name='create_expense'),
]