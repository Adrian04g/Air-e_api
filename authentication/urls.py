from django.urls import path
from .views import RegisterView, UserProfileView

urlpatterns = [
    path('user/', UserProfileView.as_view(), name='user_profile'),
    path('register/', RegisterView.as_view(), name='register'),
]