from django.forms import ModelForm
from items.models import Todolist

class TodolistForm(ModelForm):
    class Meta:
        model = Todolist
        fields = ['title', 'description', 'due_date', 'priority', 'category']