from django.urls import path
from rest_framework.routers import DefaultRouter
from . import views

urlpatterns = [
    path('list/', views.ContratoViewSet.as_view(), name='contratos-list'),
    path('detail/<int:pk>/', views.ContratoViewSet.as_view(), name='contratos-detail'),
    # contrato por cableoperador
    path('create/', views.ContratoSupabase.as_view(), name='contratos-create'),
    path('create/<int:pk>/', views.ContratoDetail.as_view(), name='contratos-create')
]