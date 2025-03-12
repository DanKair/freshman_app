from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        extra_fields.setdefault("username", email.split("@")[0])  # Default username from email
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
    FRESHMAN = 'freshman'
    MENTOR = 'mentor'
    APPLICANT = 'applicant'

    ROLE_CHOICES = [
        (APPLICANT, "Applicant"),
        (FRESHMAN, "Freshman"),
        (MENTOR, "Mentor"),
        #("admin", "Admin")
    ]
    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=25, blank=False)
    last_name = models.CharField(max_length=25, blank=False)
    phone_number = models.CharField(max_length=15, unique=True)
    role = models.CharField(max_length=15, choices=ROLE_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ["username", "first_name", "last_name", "role", "phone_number"]

    objects = UserManager()

    def __str__(self):
        return f"{self.username} with role: {self.role}"








