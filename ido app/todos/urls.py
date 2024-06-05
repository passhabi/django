from todos.views import *
from django.urls import path

urlpatterns = ([
    path('todolist/', todolist, name='todolist'),
    path('todolist/<int:id>', detailed_todo, name='todolist'),
    path('delete/', delete_todo, name='delete'),
    path('delete/<int:id>', delete_todo, name='delete'),
    path('complete/', complete_todo, name='complete'),
    path('complete/<int:id>', complete_todo, name='complete'),
    path('uncomplete/', un_complete_todo, name='uncomplete'),
    path('uncomplete/<int:id>', un_complete_todo, name='uncomplete'),
    path('add/', add_todo, name='add_todo'),

])
