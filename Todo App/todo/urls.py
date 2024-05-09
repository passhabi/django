"""
URL configuration for todo project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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

from items.views import *

urlpatterns = [
    path("", homepage, name='homepage'),
    path('admin/', admin.site.urls),
    path('todolist/', todolist, name='todolist'),
    path('todolist/<int:id>', detailed_todo, name='todolist'),
    path('delete/', delete_todo, name='delete'),
    path('delete/<int:id>', delete_todo, name='delete'),
    path('complete/', complete_todo, name='complete'),
    path('complete/<int:id>', complete_todo, name='complete'),
    path('uncomplete/', un_complete_todo, name='uncomplete'),
    path('uncomplete/<int:id>', un_complete_todo, name='uncomplete'),
    path('add/', add_todo, name='add_todo'),
    path('sign-up-in/', sign_up_in, name='signupin'),
    path('logout/', sign_out, name='logout'),
]
