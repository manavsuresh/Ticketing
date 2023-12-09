# Generated by Django 4.1 on 2023-05-02 03:10

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0015_alter_todo_unit'),
    ]

    operations = [
        migrations.AddField(
            model_name='credentials',
            name='phone',
            field=models.CharField(default='Not Given', max_length=50),
        ),
        migrations.AlterField(
            model_name='todo',
            name='date',
            field=models.CharField(auto_created=True, default=datetime.date(2023, 5, 2), max_length=255),
        ),
    ]
