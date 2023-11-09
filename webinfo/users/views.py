from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import CustomUserCreationForm
from . forms import EditProfileForm
from django.contrib.auth import authenticate, login
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .utils import generate_otp, send_otp_email
from datetime import datetime
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from . models import CustomUser

import pyotp

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
           # password = form.cleaned_data.get('password1')
           # user = authenticate(username=username, password=password)
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = CustomUserCreationForm()
        return render(request, 'users/register.html', {'form':form})
    

@login_required()
def profile(request):
    return render(request, 'users/profile.html')

class LoginWithOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        otp = generate_otp()
        user.otp = otp
        user.save()

        send_otp_email(email, otp)
        # send_otp_phone(phone_number, otp)

        return Response({'message': 'OTP has been sent to your email.'}, status=status.HTTP_200_OK)

class ValidateOTP(APIView):
    def post(self, request):
        email = request.data.get('email', '')
        otp = request.data.get('otp', '')

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return Response({'error': 'User with this email does not exist.'}, status=status.HTTP_404_NOT_FOUND)

        if user.otp == otp:
            user.otp = None  # Reset the OTP field after successful validation
            user.save()

            # Authenticate the user and create or get an authentication token
            token, _ = Token.objects.get_or_create(user=user)

            return Response({'token': token.key}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid OTP.'}, status=status.HTTP_400_BAD_REQUEST)
    
def edit_user(request, id):
    user = CustomUser.objects.get(id=id)
    return render(request, 'users/edit_profile.html', {'user':user})

def update_user(request, id):
    user = CustomUser.objects.get(id=id)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = EditProfileForm(instance=user)

    return render(request, 'users/edit_profile.html', {'user': user, 'form': form})

def admin_view(request):  
    users = CustomUser.objects.all()  
    return render(request,'users/show_users.html', {'users': users})

def delete_user(request, id):  
    user = CustomUser.objects.get(id=id)  
    user.delete()  
    return redirect('admin_view')

def dashboard(request):
    return render(request, 'users/dashboard.html')

def maps(request):
    return render(request, 'users/maps.html')
