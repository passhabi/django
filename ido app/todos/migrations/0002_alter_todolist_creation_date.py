# Generated by Django 5.0.4 on 2024-05-05 14:46

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('todos', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='todolist',
            name='creation_date',
            field=models.DateTimeField(verbose_name=datetime.datetime(2024, 5, 5, 18, 16, 1, 185050)),
        ),
    ]
