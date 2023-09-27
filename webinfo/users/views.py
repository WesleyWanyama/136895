from django.shortcuts import render , redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from . forms import CustomUserCreationForm
from . forms import EditProfileForm
from django.contrib.auth import authenticate, login
from .utils import send_otp 
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
    
#def login(request):
    #error_message = None
    #if request.method == 'POST':
        #username = request.POST['username']
        #password = request.POST['password']
        #user = authenticate(request, username=username, password=password)
        #if user is not None:
            #request.session['username'] = username
            #return redirect('otp_view') #profile
        #else:
            #error_message = 'Invalid username or password'
            #return render(request, 'login.html', {'error_message': error_message})
    
    
@login_required()
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
                totp = pyotp.TOTP(otp_secret_key, interval=60)
                if totp.veryfy(otp):
                    user = get_object_or_404(User, username=username)

                    login(request, user)

                    del request.session['otp_secret_key']
                    del request.session['otp_valid_date']

                    return redirect('home')
                
                else:
                    error_message = 'invalid one time password'
            else:
                error_message = 'one time password has expired'
        else:
            error_message = 'Something went wrong'
    return render(request, 'users/otp.html', {'error_message': error_message})

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
