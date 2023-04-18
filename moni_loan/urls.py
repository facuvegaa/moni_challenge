"""
URL configuration for moni_loan project.

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
from django.urls import path
from loan_request import views

urlpatterns = [
    path('admin_login/', views.admin_login, name="admin_login"),
    path('prestamos/', views.listar_prestamos_solicitados, name='prestamos'),
    path('', views.solicitar_prestamo, name='solicitar_prestamo'),
    path('editar_solicitud/<int:pk>/', views.editar_prestamo_solicitado, name='editar_solicitud'),
    path('eliminar_solicitud/<int:pk>/', views.eliminar_prestamo_solicitado, name='eliminar_solicitud'),
]
