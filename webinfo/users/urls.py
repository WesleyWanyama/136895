from django.urls import path
from . import views
from django.contrib.auth import views as auth_view

urlpatterns = [
    path('', views.home, name='home'),#we defined home function in views.py
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    #path('otp_view/', views.otp_view, name='otp_view'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
]
