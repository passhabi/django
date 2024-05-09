from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import login, logout, authenticate
from items.models import Todolist
from items.forms import TodolistForm

from datetime import datetime

# Create your views here.
def homepage(request):
    return render(request, "items/homepage.html")

def sign_up_in(request):
    if request.method == "GET":
        return render_sign_up_in(request)
    
    # Its a POST request:
    # Findout if its sing-up?!
    if 'password1' in request.POST:
        # Its a singpup request:
        return signup(request)
    
    # Then it is a Sing-in:
    if 'password' in request.POST:
        return sign_in(request)
        
def render_sign_up_in(request, error_msg=ValidationError(""),  sign_up_or_in=None):

    cache_email_input, signup_errors, signin_errors = "","",""
    # If there is an error:
    if error_msg != ValidationError(""):
        if sign_up_or_in is "in":
            signin_errors = error_msg
        elif sign_up_or_in is "up":
            cache_email_input = request.POST['email'] # cashe the email in the template form.
            signup_errors = error_msg
        else:
            raise ValueError("Either wrong value or no value set for the sign_up_or_in argument. The value must be set either 'in' or 'up' if the error_msg has been set.")
        

    assert(type(error_msg) == ValidationError)



    return render(request, 'items\sign-up-in.html', {'signup_form': UserCreationForm(),
                                                     'signin_form': AuthenticationForm(),
                                                     'signup_errors': signup_errors,
                                                     'signin_errors': signin_errors,
                                                     'cache_email_input': cache_email_input,
                                                    })

def signup(request):
    "(POST) Registering the new user:"    
    if request.POST['password1'] != request.POST['password2']:
        return render_sign_up_in(request, error_msg=ValidationError("The passwords you entered don't match."), sign_up_or_in='up')
    
    username = request.POST['username']
    password = request.POST['password1']
    email = request.POST['email']

    # Validate and store into the database:
    try:
        validate_password(request.POST['password1'])

        # user = User.objects.create_user(username=username, email=email, password=password)
        user = User(username=username, email=email)
        user.set_password(password)
        user.save()

        login(request, user)

    except IntegrityError:
         return render_sign_up_in(request, ValidationError("The username exists. Choose another username."), 'up')
    
    except ValidationError as error_list:
         return render_sign_up_in(request, error_msg=error_list, sign_up_or_in='up')
    
    return redirect('todolist')

def sign_in(request):
    user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
    if user is None:
        return render_sign_up_in(request, ValidationError("The combination of username and password do not exist."), 'in')
    
    login(request, user)
    return redirect('todolist')

def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('homepage')
    return redirect('homepage')


def todolist(request):
     # if the user is not athuraized.
     if not request.user.id:
        raise PermissionDenied
    
     todo_items = Todolist.objects.filter(user = request.user, completion_time=None)
     completed_todos = Todolist.objects.filter(user = request.user). exclude(completion_time=None)
     return render(request, r'items\todolist.html', {'todo_items': todo_items, 'completed_todos': completed_todos})
     
def detailed_todo(request, id):
    todo  = get_object_or_404(Todolist, pk=id, user=request.user)

    if request.method == 'GET':
        filled_form = TodolistForm(instance=todo)
        return render(request, "items/edit.html", {'form': filled_form})
    
    # POST:
    todolist_form = TodolistForm(request.POST, instance=todo)
    todolist_form.save()
    return redirect('todolist')


def add_todo(request):
    if request.method == 'GET':
        return render(request, 'items/todolist_additem.html', {'todo_additem_form': TodolistForm()})

    newitem = TodolistForm(request.POST)
    newitem.save(commit=False).user = request.user
    newitem.save()
    return redirect('todolist')

def delete_todo(request, id):
    if request.method == 'GET':
        return redirect('todolist')
    
    return redirect('todolist')


def complete_todo(request, id):
    if request.method == 'GET':
        return redirect('todolist')

    todo = Todolist.objects.filter(id=id, user=request.user)
    todo.update(completion_time=datetime.now())
    
    return redirect('todolist')


def un_complete_todo(request, id):
    if request.method == 'GET':
        return redirect('todolist')

    todo = Todolist.objects.filter(id=id, user=request.user)
    todo.update(completion_time=None)
    
    return redirect('todolist')


