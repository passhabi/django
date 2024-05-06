from django.db import models
from datetime import datetime
from django.contrib.auth.models import User



PRIORITY_CHOICES = {
    "MR": 1,
    "MRS": 2,
    "MS": 3,
    "MS": 4,
}


# Create your models here.
class Todolist(models.Model):
    title = models.CharField(null=False,blank=False, max_length=300)
    description = models.TextField(blank=True)
    due_date= models.DateTimeField(blank=True)
    priority = models.SmallIntegerField(blank=True, choices=[1,2,3,4])
    category = models.IntegerField(blank=True)

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    creation_date = models.DateTimeField(auto_now_add=True)
    completion_time = models.DateTimeField(null=True, blank=True)  

    def __str__(self) -> str:
        return self.title