from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import login, logout, authenticate
from todos.models import Todolist, Features
from todos.forms import TodolistForm
from django.contrib.auth.decorators import login_required

from datetime import datetime


# Create your views here.
def homepage(request):
    features = Features.objects.all()

    return render(request, "index.html", {'features': features})


def signin(request):
    if request.method == "POST":
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user:
            login(request, user)
            return redirect('todolist')
        else:
            return render(request, 'sign-in.html',
                          {'errors': ["The combination of username and password do not exist.", ]})

    # It's a GET
    return render(request, 'sign-in.html')


def signup(request):
    # GET
    return render(request, template_name='sign-up.html')
    "(POST) Registering the new user:"
    if request.POST['password1'] != request.POST['password2']:
        return render_sign_in(request, error_msg=ValidationError("The passwords you entered don't match."),
                              sign_up_or_in='up')

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

    return redirect('homepage')


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect('homepage')
    return redirect('homepage')


@login_required(redirect_field_name='signupin')
def todolist(request):
    todo_items = Todolist.objects.filter(user=request.user, completion_time=None)
    completed_todos = Todolist.objects.filter(user=request.user).exclude(completion_time=None)
    return render(request, r'todolist.html', {'todo_items': todo_items, 'completed_todos': completed_todos})


@login_required
def detailed_todo(request, id):
    todo = get_object_or_404(Todolist, pk=id, user=request.user)

    if request.method == 'GET':
        filled_form = TodolistForm(instance=todo)
        return render(request, "items/edit.html", {'form': filled_form})

    # POST:
    todolist_form = TodolistForm(request.POST, instance=todo)
    todolist_form.save()
    return redirect('todolist')


@login_required
def add_todo(request):
    if request.method == 'GET':
        return render(request, 'items/todolist_additem.html', {'todo_additem_form': TodolistForm()})

    newitem = TodolistForm(request.POST)
    newitem.save(commit=False).user = request.user
    newitem.save()
    return redirect('todolist')


@login_required
def delete_todo(request, id):
    if request.method == 'GET':
        return redirect('todolist')

    todo = get_object_or_404(Todolist, id=id, user=request.user)
    todo.delete()

    return redirect('todolist')


@login_required
def complete_todo(request, id):
    if request.method == 'GET':
        return redirect('todolist')

    todo = Todolist.objects.filter(id=id, user=request.user)
    todo.update(completion_time=datetime.now())

    return redirect('todolist')


@login_required
def un_complete_todo(request, id):
    if request.method == 'GET':
        return redirect('todolist')

    todo = Todolist.objects.filter(id=id, user=request.user)
    todo.update(completion_time=None)

    return redirect('todolist')


@login_required
def profile(request):
    return HttpResponse(f"Dear {request.user}<p>Your profile is not available for now. try again later...")
