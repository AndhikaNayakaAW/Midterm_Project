from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    group_choice = forms.ChoiceField(
        choices=[('user', 'User'), ('admin', 'Admin')],
        widget=forms.RadioSelect
    )

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'group_choice']

