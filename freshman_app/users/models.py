from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ("applicant", "Applicant"),
        ("freshman", "Freshman"),
        ("mentor", "Mentor"),
    ]
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25)
    last_name = models.CharField(max_length=25)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='applicant')
    created_at = models.DateTimeField(auto_now_add=True)