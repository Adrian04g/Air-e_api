from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('list/', views.ContratoViewSet.as_view(), name='contratos-list'),
    path('list/<int:pk>/', views.ContratoDetailViewSet.as_view(), name='contratos-detail'),
]