from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('game:login')),  # Redirect root to login
    path('game/', include('game.urls')),
]