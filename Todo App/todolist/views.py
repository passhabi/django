from django.shortcuts import render, HttpResponse, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.contrib.auth import login


# Create your views here.
def homepage(request):
    return HttpResponse("<h1> Home Page </h1> <p> <a href='singup/'> Sing Up </a>")

def signup(request):
    if request.method == 'GET':
         return signup_render(request)
    
    "(POST) Registering the new user:"    
    if request.POST['password1'] != request.POST['password2']:
        return signup_render(request, ["The passwords you entered don't match."])
    
    username = request.POST['username']
    password = request.POST['password1']
    email = request.POST['email']

    # Validate and store into the database:
    try:
        validate_password(request.POST['password1'])

        user = User(username=username, email=email, password=password)
        user.save()

        login(request, user)

    except IntegrityError:
         return signup_render(request, ["The username exists. Choose another username."])
    
    except ValidationError as error_list:
         return signup_render(request, error_msg_list=error_list)
    
    return redirect('signedup')


def signup_render(request, error_msg_list=[]):
        
        email = ""
        if error_msg_list:
            email = request.POST['email']
            

        print(error_msg_list)
        print(type(error_msg_list))
        print(list)
        print(type(list))

        assert(type(error_msg_list) == list)

        return render(request, 'todolist\signup.html', {'django_form': UserCreationForm(),
                                                        'error_message': error_msg_list,
                                                        'cache_email_input': email})

def signedup(request):
     return render(request, 'todolist\signedup.html')