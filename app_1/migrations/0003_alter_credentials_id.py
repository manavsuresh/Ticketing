# Generated by Django 4.1 on 2022-08-26 07:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_1', '0002_credentials_id_alter_credentials_u_id_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='credentials',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, unique=True),
        ),
    ]
