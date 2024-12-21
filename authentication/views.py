from django.contrib.auth import authenticate, login as auth_login
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
import json
from django.contrib.auth.decorators import login_required


from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.http import JsonResponse
import json
from django.core.exceptions import ValidationError
import re

def is_valid_email(email):
    # Simple email validation regex
    return re.match(r"[^@]+@[^@]+\.[^@]+", email) is not None

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Validate the input
        if not username or not password:
            return JsonResponse({
                "status": False,
                "message": "Username and password are required."
            }, status=400)

        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                auth_login(request, user)
                return JsonResponse({
                    "username": user.username,
                    "status": True,
                    "message": "Login successful!"
                }, status=200)
            else:
                return JsonResponse({
                    "status": False,
                    "message": "Login failed, account disabled."
                }, status=401)
        else:
            return JsonResponse({
                "status": False,
                "message": "Invalid credentials. Check username or password."
            }, status=401)
    else:
        return JsonResponse({
            "status": False,
            "message": "Invalid request method."
        }, status=400)

def register_view(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        email = data.get('email')
        password1 = data.get('password1')
        password2 = data.get('password2')

        # Validate inputs
        if not username or not email or not password1 or not password2:
            return JsonResponse({
                "status": False,
                "message": "All fields are required."
            }, status=400)

        if password1 != password2:
            return JsonResponse({
                "status": False,
                "message": "Passwords do not match."
            }, status=400)

        if not is_valid_email(email):
            return JsonResponse({
                "status": False,
                "message": "Invalid email format."
            }, status=400)

        if User.objects.filter(username=username).exists():
            return JsonResponse({
                "status": False,
                "message": "Username already exists."
            }, status=400)

        if User.objects.filter(email=email).exists():
            return JsonResponse({
                "status": False,
                "message": "Email already exists."
            }, status=400)

        # Create user
        try:
            user = User.objects.create_user(username=username, email=email, password=password1)
            user.save()
            return JsonResponse({
                "username": user.username,
                "status": 'success',
                "message": "User created successfully!"
            }, status=200)

        except ValidationError as e:
            return JsonResponse({
                "status": False,
                "message": f"Error: {str(e)}"
            }, status=400)

    return JsonResponse({
        "status": False,
        "message": "Invalid request method."
    }, status=400)


@csrf_exempt
def profile(request):
    return JsonResponse({
        "status": "success",
        "data": {
            "username": request.user.username,
            "email": request.user.email,
        }
    })
