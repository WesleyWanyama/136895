from django.urls import path
from . import views

urlpatterns = [
    path('', views.home) #we defined home function in views.py
]
