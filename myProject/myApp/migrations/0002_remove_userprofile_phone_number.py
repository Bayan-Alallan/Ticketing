# Generated by Django 5.1.1 on 2024-10-09 20:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myApp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='Phone_Number',
        ),
    ]
