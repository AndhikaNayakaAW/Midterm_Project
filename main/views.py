from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from main.models import Restaurants, Quotes
from main.forms import RestoEntryForm
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
import datetime
from django.urls import reverse
from django.core.paginator import Paginator
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from main.forms import ContactUsForm
from main.models import Contact
from django.contrib.auth.decorators import user_passes_test
from user_role.views import admin_check
from user_role.forms import CustomUserCreationForm
from django.contrib.auth.models import Group
from reviews.models import Review
from reviews.forms import ReviewForm



def show_main(request):
    resto_entries = Restaurants.objects.all()  # Ensure the correct model is used

    # Implement pagination
    paginator = Paginator(resto_entries, 6)  # Show 6 restaurants per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        "name": request.user.username,
        "resto_entries": page_obj,  # Pass the paginated entries to the template
        "last_login": request.COOKIES.get("last_login", "Not set"),
    }

    return render(request, "main.html", context)

@login_required(login_url="/login")
def pagination_json(request):
    resto_entries = Restaurants.objects.all()  # Ensure the correct model is used

    # Implement pagination
    paginator = Paginator(resto_entries, 6)  # Show 6 restaurants per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return HttpResponse(
        serializers.serialize("json", page_obj), content_type="application/json"
    )

@login_required(login_url="/login")
@user_passes_test(admin_check)
def create_restaurant_entry(request):
    form = RestoEntryForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        restaurant_entry = form.save(commit=False)
        restaurant_entry.user = request.user
        restaurant_entry.save()
        return redirect("main:show_main")

    context = {"form": form}
    return render(request, "create_new_resto.html", context)

@login_required(login_url="/login")
@user_passes_test(admin_check)
def show_xml(request):
    data = Restaurants.objects.all()
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )

@login_required(login_url="/login")
@user_passes_test(admin_check)
def show_json(request):
    data = Restaurants.objects.all()
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )

@login_required(login_url="/login")
@user_passes_test(admin_check)
def show_xml_by_id(request, id):
    data = Restaurants.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("xml", data), content_type="application/xml"
    )

@login_required(login_url="/login")
@user_passes_test(admin_check)
def show_json_by_id(request, id):
    data = Restaurants.objects.filter(pk=id)
    return HttpResponse(
        serializers.serialize("json", data), content_type="application/json"
    )

@login_required(login_url="/login")
@user_passes_test(admin_check)
def edit_restaurant(request, id):
    item = Restaurants.objects.get(pk=id)
    form = RestoEntryForm(request.POST or None, instance=item)
    if form.is_valid() and request.method == "POST":
        form.save()
        return HttpResponseRedirect(reverse("main:show_main"))
    context = {"form": form}
    return render(request, "edit_resto.html", context)

@login_required(login_url="/login")
@user_passes_test(admin_check)
def delete_restaurant(request, id):
    item = Restaurants.objects.get(pk=id)
    item.delete()
    return HttpResponseRedirect(reverse("main:show_main"))


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()

            # Assign the user to the selected group
            selected_group = form.cleaned_data.get('group')
            group = Group.objects.get(name=selected_group)
            user.groups.add(group)

            return redirect('/login')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)
            response = HttpResponseRedirect(reverse("main:show_main"))
            response.set_cookie("last_login", str(datetime.datetime.now()))
            return response

    else:
        form = AuthenticationForm(request)
    context = {"form": form}
    return render(request, "login.html", context)

@login_required(login_url="/login")
def logout_user(request):
    logout(request)
    response = HttpResponseRedirect(reverse("main:login"))
    response.delete_cookie("last_login")
    return response

def restaurant_details(request, id):
    restaurant = get_object_or_404(Restaurants, id=id)
    reviews = Review.objects.filter(restaurant=restaurant)

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user  # Automatically assign the logged-in user
            review.restaurant = restaurant  # Automatically assign the restaurant
            review.save()
            return redirect('restaurant_details', id=restaurant.id)  # Redirect to avoid resubmission
    else:
        form = ReviewForm()

    context = {
        'restaurant': restaurant,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'restaurant_detail.html', context)
@login_required(login_url="/login")
@csrf_exempt
def submit_quote(request):
    if request.method == "POST":
        quote_content = request.POST.get('content')
        new_quote = Quotes.objects.create(content=quote_content)
        quotes = list(Quotes.objects.all().order_by('-created_at').values('content'))
        return JsonResponse({'quotes': quotes}, status=200)
    
    return JsonResponse({'error': 'Invalid request method'}, status=400)

def show_contact(request):
    return render(request, "contact_us.html")

def contact_request(request):
    form = ContactUsForm(request.POST or None)

    if form.is_valid() and request.method == "POST":
        form.save()
        return redirect('main:show_main')

    context = {'form': form}
    return render(request, "contact_us.html", context)