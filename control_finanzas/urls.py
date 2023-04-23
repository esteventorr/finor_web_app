from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_menu, name='main_menu'),
    path('crear-gastos/', views.ingresar_gastos, name='crear_gastos'),
    path('create_expense/', views.create_expense, name='create_expense'),
    path('metas-ahorros/', views.ingresar_objetivos, name='metas_ahorros'),
    path('analisis-gastos/', views.analisis_gastos, name='analisis_gastos'),
    path('mensajes-alertas/', views.mensajes_alertas, name='mensajes_alertas'),
    path('create_goal/', views.create_goal, name='create_goal'),
    path('create_reminder/', views.create_reminder, name='create_reminder'),
    path('calendario/', views.calendario, name='calendario'),
]
