from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from main.models import Restaurants
from main.forms import RestoEntryForm

def show_main(request):
    resto_entries = Restaurants.objects.all()

    context = {
        'resto_entries': resto_entries
    }

    return render(request, "main.html", context)

def create_restaurant_entry(request):
    form = RestoEntryForm(request.POST or None)
    if form.is_valid() and request.method == "POST":
        form.save()
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