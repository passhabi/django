from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.


def signup(request):
    return render(request, 'todolist\signup.html', {'django_form': UserCreationForm()})