from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from . import views

urlpatterns = [
    path('list/', views.CableoperadoresList.as_view(), name='cableoperadores-list'),
    path('detail/<int:pk>/', views.CableoperadoresDetail.as_view(), name='cableoperadores-detail'),
    #path('login/', obtain_auth_token, name='api_token_auth'),
]
