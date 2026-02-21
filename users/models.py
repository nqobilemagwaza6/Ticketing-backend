from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (
        ('User', 'User'),
        ('Support', 'Support'),
        ('Admin', 'Admin'),
    )
    email = models.EmailField(unique=True) # <- Make emails unique
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='User')

    def __str__(self):
        return f"{self.username} ({self.role})"