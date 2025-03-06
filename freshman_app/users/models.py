from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    ROLE_CHOICES = [
        ("applicant", "Applicant"),
        ("freshman", "Freshman"),
        ("mentor", "Mentor"),
        ("admin", "Admin")
    ]
    username = None
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES, default='applicant')
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["first_name", "last_name", "role", "phone_number"]

    objects = UserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} with role: {self.role}"


