from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
	class UserRole(models.TextChoices):
		ADMIN = 'admin'
		TEACHER = 'teacher'
		STUDENT = 'student'
	
	username = None
	email = models.EmailField(max_length=255, unique=True)
	full_name = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	role = models.CharField(choices=UserRole.choices, default=None, null=True, max_length=10)
	is_pending = models.BooleanField(default=True)

	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = []