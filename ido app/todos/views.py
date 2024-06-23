from django.shortcuts import render, HttpResponse, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError, PermissionDenied
from django.contrib.auth import login, logout, authenticate
from todos.models import Todolist, UserSetting
from todos.forms import TodolistForm
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from datetime import datetime


# Create your views here.
def homepage(request):
    return render(request, "index.html")


def signin(request):
    if request.method == "POST":
        user = authenticate(
            request,
            username=request.POST["username"],
            password=request.POST["password"],
        )
        if user:
            login(request, user)
            return redirect("list_todos")
        else:
            return render(
                request,
                "sign-in.html",
                {
                    "errors": [
                        "The combination of username and password do not exist.",
                    ]
                },
            )

    # It's a GET
    return render(request, "sign-in.html")


def signup(request):
    # (GET)
    if request.method == "GET":
        return render(request, template_name="sign-up.html")

    # (POST) Registering the new user:
    errors = {
        "firstname": "is-valid",  # bootstrap class
        "lastname": "is-valid",
        "email": "is-valid",
        "username": "is-valid",
        "password1": "is-invalid",
        "password2": "is-invalid",
        "password_details": [],
    }

    values = {
        "firstname": request.POST["firstname"],
        "lastname": request.POST["lastname"],
        "username": request.POST["username"],
        "email": request.POST["email"],
    }

    try:
        validate_password(request.POST["password1"])
        assert request.POST["password1"] == request.POST["password2"]
        # bugs: the password week messages doesn't show up!
    except ValidationError as messages:
        errors["password_details"] = messages
        return render(
            request,
            template_name="sign-up.html",
            context={"errors": errors, "values": values},
        )

    except AssertionError:
        errors["password_details"] = ["password does not match"]
        return render(
            request,
            template_name="sign-up.html",
            context={"errors": errors, "values": values},
        )

    try:
        user = User.objects.create_user(
            request.POST["username"], request.POST["email"], request.POST["password1"]
        )
    except IntegrityError:
        errors["username"] = "is-invalid"
        return render(
            request,
            template_name="sign-up.html",
            context={"errors": errors, "values": values},
        )

    user.first_name = request.POST["firstname"]
    user.last_name = request.POST["lastname"]
    user.usersetting = UserSetting.objects.create(user=user, )
    user.save()

    login(request, user)
    return redirect("homepage")


def sign_out(request):
    if request.method == "POST":
        logout(request)
        return redirect("homepage")
    return redirect("homepage")


def reverse_the_order(request, is_dec):
    pass


@login_required(login_url="login")
def order_it_by(request):
    user = User.objects.get(username=request.user)

    user.usersetting.order_by = request.POST['orderby'][0]  # take the first letter. e.g. title >>> 't'
    user.usersetting.save()

    return list_todos(request)


@login_required(login_url="login")
def reverse_the_order(request):
    user = User.objects.get(username=request.user)
    user.usersetting.is_descending = not user.usersetting.is_descending
    user.usersetting.save()

    return list_todos(request)


@login_required(redirect_field_name="login")
def list_todos(request):
    user = User.objects.get(username=request.user)
    user_view_settings = user.usersetting

    todo_items = Todolist.objects.filter(user=request.user, completion_time=None)

    # add view settings to template:
    query_str = '-'
    if user_view_settings.is_descending:
        query_str = ''
    query_str += user_view_settings.ORDER_BY_CHOICES[user_view_settings.order_by]

    todo_items = todo_items.order_by(query_str)  # sort items by query_set

    return render(
        request,
        r"list_todos.html",
        {"todo_items": todo_items,
         "user_view_settings": user_view_settings, },
    )


@login_required
def detailed_todo(request, id):
    todo = get_object_or_404(Todolist, pk=id, user=request.user)

    if request.method == "GET":
        return render_edit_page(request, todo)

    # POST:
    if request.POST["button"] == "complete_button":
        return make_as_completed(request, id)

    if request.POST["button"] == "save_button":
        todolist_form = TodolistForm(request.POST, instance=todo)
        todolist_form.save()

        todo = get_object_or_404(Todolist, pk=id, user=request.user)
        return render_edit_page(request, todo, True)

    if request.POST["button"] == "delete":
        todolist_form = TodolistForm(request.POST, instance=todo)
        todo.delete()

        return redirect('list_todos')


def render_edit_page(request, todo, saved: bool = False):
    if todo.priority:
        todo.__dict__["priority_radio_select" + str(todo.priority)] = (
            "checked"  # this is the html radio tag 'checked'.
        )
    todo.__dict__["category_option" + str(todo.category)] = (
        "selected"  # this is the html tag.
    )
    return render(
        request, "edit.html", context={"todo": todo, "has_been_saved": saved}
    )


@login_required
def add_todo(request):
    if request.method == "GET":
        # todo: send categories to template.
        return render(request, "add_todo.html")

    # bug: repated todos could be saved.
    newitem = TodolistForm(request.POST)
    newitem.save(commit=False).user = request.user
    newitem.save()

    return render(
        request, "add_todo.html", context={"added_todo": request.POST["title"]}
    )


@login_required
def delete_todo(request, id):
    if request.method == "GET":
        return redirect("list_todos")

    todo = get_object_or_404(Todolist, id=id, user=request.user)
    todo.delete()

    return redirect("list_todos")


@login_required
def list_completed_todos(request):
    if request.method == "GET":
        completed_todos = Todolist.objects.filter(completion_time__isnull=False).order_by('-completion_time')
        completed_todos = list(completed_todos)
        return render(request, 'completed.html', context={'completed_todos': completed_todos})

    # todo = Todolist.objects.filter(id=id, user=request.user)
    # todo.update(completion_time=datetime.now())

    # return redirect("list_todos")


@login_required
def un_complete_todos(request, id):
    todo = Todolist.objects.filter(id=id, user=request.user)
    todo.update(completion_time=None)

    return redirect("completed")


def make_as_completed(request, id):
    todo = get_object_or_404(Todolist, pk=id, user=request.user)

    todo.completion_time = datetime.now()
    todo.save()
    return redirect("list_todos")


@login_required
def profile(request):
    return HttpResponse(
        f"Dear {request.user}<p>Your profile is not available for now. try again later..."
    )
