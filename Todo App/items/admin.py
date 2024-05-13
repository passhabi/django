from django.contrib import admin
from items.models import Todolist, Features


class TodolistAdmin(admin.ModelAdmin):
    readonly_fields = ['creation_date', ]


# Register your models here.
admin.site.register(Todolist, TodolistAdmin)
admin.site.register(Features)
