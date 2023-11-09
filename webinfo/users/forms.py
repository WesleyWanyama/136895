from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class EditProfileForm(forms.ModelForm):
    USER_TYPE_CHOICES = [
        ('researcher', 'Researcher'),
        ('health_official', 'Health Official'),
    ]
    user_type = forms.ChoiceField(choices=USER_TYPE_CHOICES, widget=forms.Select(attrs={'class': 'form-control'}))
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'user_type']

class FileUploadForm(forms.Form):
    file = forms.FileField()

