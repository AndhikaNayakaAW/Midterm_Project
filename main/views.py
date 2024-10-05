from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from main.models import Restaurants
from main.forms import RestoEntryForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from django.urls import reverse


@login_required(login_url='/login')
def show_main(request):
    resto_entries = Restaurants.objects.filter(user=request.user)

    context = {
        'name': request.user.username,
        'resto_entries': resto_entries,
        'last_login': request.COOKIES.get('last_login', 'Not set'),
    }

    return render(request, "main.html", context)

def create_restaurant_entry(request):
    form = RestoEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        restaurant_entry = form.save(commit=False)
        restaurant_entry.user = request.user
        restaurant_entry.save()
        return redirect('main:show_main')
    
    context = {'form': form}
    return render(request, "create_new_resto.html", context)

def show_xml(request):
    data = Restaurants.objects.all()
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json(request):
    data = Restaurants.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def show_xml_by_id(request, id):
    data = Restaurants.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("xml", data), content_type="application/xml")

def show_json_by_id(request, id):
    data = Restaurants.objects.filter(pk=id)
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def edit_restaurant(request, id):
    item = Restaurants.objects.get(pk = id)
    form = RestoEntryForm(request.POST or None, instance=item)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse('main:show_main'))
    context = {'form': form}
    return render(request, "edit_resto.html", context)

def delete_restaurant(request, id):
    item = Restaurants.objects.get(pk = id)
    item.delete()
    return HttpResponseRedirect(reverse('main:show_main'))

def register(request):
    form = UserCreationForm()

    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your account has been successfully created!')
            return redirect('main:login')
    context = {'form':form}
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
    response = HttpResponseRedirect(reverse('main:login'))
    response.delete_cookie('last_login')
    return response

