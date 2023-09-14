from django.shortcuts import render , redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import UserRegisterForm
from django.contrib.auth import authenticate, login
from .utils import send_otp 
from datetime import datetime
import pyotp

def home(request):
    return render(request, 'users/home.html')

def register(request):
    if request.method == "POST":
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            messages.success(request, f'Hi {username}, your account was created successfully')
            return redirect('home')
    else:
        form = UserRegisterForm()
        return render(request, 'users/register.html', {'form':form})
    

def profile(request):
    return render(request, 'users/profile.html')

def otp_view(request):
    error_message = None
    if request.method == 'POST':
        otp = request.POST['otp']
        username = request.session['username']

        otp_secret_key = request.session['otp_secret_key']
        otp_valid_date = request.session['otp_valid_date']

        if otp_secret_key and otp_valid_date is not None:
            valid_date = datetime.fromisoformat(otp_valid_date)

            if valid_date > datetime.now():
                totp = pyotp
    return render(request, 'otp.html', {})
