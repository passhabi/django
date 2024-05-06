from django.contrib import admin
from items.models import Todolist

class ToodlistAdmin(admin.ModelAdmin):
   readonly_fields = ['creation_date', ]

# Register your models here.
admin.site.register(Todolist, ToodlistAdmin)