from django.db import models

# Create your models here.
class Assignment(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	due_date = models.DateField()
	created_at = models.DateField(auto_now_add=True)
	classroom = models.ForeignKey('classrooms.Classroom', on_delete=models.CASCADE, related_name='assignments')
	created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='assignments')


class Comment(models.Model):
	content = models.TextField()
	created_at = models.DateField(auto_now_add=True)
	assignment = models.ForeignKey('assignments.Assignment', on_delete=models.CASCADE, related_name='comments')
	created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='comments')


class Submission(models.Model):
	link = models.URLField()
	created_at = models.DateField(auto_now_add=True)
	assignment = models.ForeignKey('assignments.Assignment', on_delete=models.CASCADE, related_name='submissions')
	created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='submissions')