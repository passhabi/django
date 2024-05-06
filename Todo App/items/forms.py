from django.forms import ModelForm
from items.models import Todolist

class TodolistForms(ModelForm):
    class Meta:
        model = Todolist
        fields = ['title', 'description', 'due_date', 'priotity', 'category']