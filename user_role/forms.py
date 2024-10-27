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

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("This username is already taken.")
        return username