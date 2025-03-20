"""
URL configuration for mi_proyecto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', RedirectView.as_view(url='login/')),  # Redirige la raíz al login
    #path('', RedirectView.as_view(url='usuarios/login/')),  # Redirige a /usuarios/login/
    #path('', views.login_view, name='login'),  # Esto mueve el login a /usuarios/
    path('', include('usuarios.urls')),  # Incluye las URLs de la aplicación 'usuarios'
    path('folios/', include('folios.urls')),  # Incluye las URLs de la aplicación 'folios'
]