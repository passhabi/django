from django.shortcuts import render, HttpResponse
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def homepage(request):
    return HttpResponse("<h1> Home Page </h1> <p> <a href='singup/'> Sing Up </a>")

def signup(request):
    return render(request, 'todolist\signup.html', {'django_form': UserCreationForm()})