from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),#we defined home function in views.py
    path('register/', views.register, name='register')
]
