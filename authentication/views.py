import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import Group
from django.contrib.auth.forms import AuthenticationForm
from authentication.forms import CustomUserCreationForm

def register(request):
    form = CustomUserCreationForm()

    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Add user to the appropriate group
            group_choice = form.cleaned_data.get('group_choice')
            if group_choice == 'user':
                group = Group.objects.get(name='User')
            elif group_choice == 'admin':
                group = Group.objects.get(name='Admin')

            user.groups.add(group)
            messages.success(request, 'Your account has been successfully created!')
            return redirect('auth:login')

    context = {'form': form}
    return render(request, 'register.html', context)


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie('last_login', str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse('auth:login'))
    response.delete_cookie('last_login')
    return response