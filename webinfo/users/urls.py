from django.urls import path
from . import views
from django.contrib.auth import views as auth_view
from .views import LoginWithOTP, ValidateOTP

urlpatterns = [
    path('', views.home, name='home'),#we defined home function in views.py
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('maps/', views.maps, name='maps'),
    path('admin_view/', views.admin_view, name='admin_view'),
    path('upload/', views.upload_file, name='upload_file'),
    path('upload_success/', views.upload_success, name='upload_success'),
    path('edit_user/<int:id>', views.edit_user, name='edit_user'),  
    path('update_user/<int:id>', views.update_user, name='update_user'),
    path('login-with-otp/', LoginWithOTP.as_view(), name='login-with-otp'),
    path('validate-otp/', ValidateOTP.as_view(), name='validate-otp'),
    path('delete_user/<int:id>', views.delete_user, name='delete_user'),
    path('login/', auth_view.LoginView.as_view(template_name='users/login.html'), name="login"),
    path('logout/', auth_view.LogoutView.as_view(template_name='users/logout.html'), name="logout"),
]
