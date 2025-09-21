from django.urls import path
from . import views

urlpatterns = [
    path('driver/register/', views.driver_register, name='driver_register'),
    path('driver/login/', views.driver_login, name='driver_login'),
]
