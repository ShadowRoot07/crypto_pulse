from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.views.generic.base import RedirectView
from django.conf import settings
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('tracker.urls')),
    
    # Manejo del Favicon para evitar errores 404 en logs
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),

    # Rutas para el login/logout
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

