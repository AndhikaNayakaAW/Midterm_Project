# a_thousand_flavours/urls.py
from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls', namespace='main')),  # Main app
    path('favorites/', include('favorites.urls', namespace='favorites')),  # Favorites app with namespace
    # Include other apps here
]
