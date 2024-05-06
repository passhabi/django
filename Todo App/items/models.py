from django.db import models
from datetime import datetime
from django.contrib.auth.models import User


PRIORITY_CHOICES = {
    1: 'Important and Urgent',
    2: 'Important',
    3: 'Urgent',
    4: 'Not Urgent, Important',
}

# Create your models here.
class Todolist(models.Model):
    title = models.CharField(null=False,blank=False, max_length=300)
    description = models.TextField(blank=True)
    due_date= models.DateTimeField(blank=True)
    priority = models.SmallIntegerField(blank=True, choices=PRIORITY_CHOICES)
    category = models.IntegerField(blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_time = models.DateTimeField(null=True, blank=True)  

    def __str__(self) -> str:
        return self.title