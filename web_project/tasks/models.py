from django.db import models

# Create your models here.
class Task(models.Model):
	class TaskPriority(models.TextChoices):
		LOW = 'low'
		MEDIUM = 'medium'
		HIGH = 'high'

	title = models.CharField(max_length=255)
	description = models.TextField()
	priority = models.CharField(choices=TaskPriority.choices, default=TaskPriority.LOW, max_length=10)
	is_done = models.BooleanField(default=False)
	created_at = models.DateField(auto_now_add=True)
	teacher = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='tasks')
	