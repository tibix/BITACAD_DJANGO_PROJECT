"""magazin URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from produse import views as pv
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', pv.index, name='index'),
    path('entry/<int:produs_id>/', pv.entry_detail, name='entry'),
    path('contact/', pv.contact, name='contact'),
    #path('contact/', pv.Contact.as_view(), name='contact'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='logout.html'), name='logout'),
    path('profil/', pv.profil, name='profil'),
    path('cos/', pv.cos, name='cos'),
    path('adauga_cos/<int:produs_id>/', pv.adauga_in_cos, name='adauga_cos'),
    path('istoric/', pv.istoric, name='istoric'),
    path('comanda/', pv.comanda, name='comanda'),
]
