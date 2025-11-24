from django.urls import path
from .views import *

urlpatterns = [
    path('', InspectoresView.as_view(), name='inspectores-list'),
    path('<int:pk>/', SingleInspectoresView.as_view(), name='inspectores-detail'),
]