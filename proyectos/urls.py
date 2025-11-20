from django.urls import path
from . import views
urlpatterns = [
    path('ingreso/', views.IngresoProyectoView.as_view(), name='ingreso-proyectos'),
    path('ingreso/<str:pk>/', views.SingleIngresoProyectoView.as_view(), name='single-ingreso-proyecto'),
    path('list/', views.ProyectosView.as_view(), name='proyectos'),
    path('<str:pk>/', views.SingleProyectoView.as_view(), name='single-proyecto'),
]