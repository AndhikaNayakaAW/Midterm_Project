from django.urls import path
from authentication.views import login, register, profile

app_name = 'authentication'

urlpatterns = [
    path('login/', login, name='login'),
    path('register/', register, name='register'),
    path('api/profile/', profile, name='profile'),
]