from todos.views import *
from django.urls import path

urlpatterns = ([
    path('list/', list_todos, name='list_todos'),
    path('item/', detailed_todo, name='item'),
    path('item/<int:id>', detailed_todo, name='item'),
    path('delete/', delete_todo, name='delete'),
    path('delete/<int:id>', delete_todo, name='delete'),
    path('completed/', completed_todos, name='completed'),
    path('completed/<int:id>', completed_todos, name='completed'),
    path('uncompleted/', un_completed_todos, name='uncompleted'),
    path('uncompleted/<int:id>', un_completed_todos, name='uncompleted'),
    path('add/', add_todo, name='add'),

])
