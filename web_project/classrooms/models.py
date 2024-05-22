from django.db import models

# Create your models here.
class Classroom(models.Model):
	name = models.CharField(max_length=255)
	teacher = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='classrooms_monitored')
	students = models.ManyToManyField('authentication.User', related_name='classrooms_joined')