from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser


class User_Info(models.Model):
    username=models.CharField(max_length=200)
    email=models.CharField(max_length=200, unique=True)
    id=models.CharField(max_length=100,primary_key=True)

class UserProfile(AbstractUser):
    email = models.CharField(max_length=200, unique=True)

    # Avoid reverse accessor conflicts by specifying a unique related_name
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='userprofile_set',  # Unique related_name for UserProfile.groups
        blank=True,
        help_text='The groups this user belongs to.'
    )



    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='userprofile_permissions',  # Unique related_name for UserProfile.permissions
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def __str__(self):
        return self.username + self.email