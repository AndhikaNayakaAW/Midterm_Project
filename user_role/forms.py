from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group

class CustomUserCreationForm(UserCreationForm):
    GROUP_CHOICES = [
        ('User', 'User'),
        ('Admin', 'Admin'),
    ]
    
    group = forms.ChoiceField(choices=GROUP_CHOICES, required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'group']
