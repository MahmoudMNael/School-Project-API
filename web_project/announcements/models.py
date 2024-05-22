from django.db import models

# Create your models here.
class Announcement(models.Model):
	title = models.CharField(max_length=100)
	content = models.TextField()
	created_at = models.DateField(auto_now_add=True)
	classroom = models.ForeignKey('classrooms.Classroom', on_delete=models.CASCADE, related_name='announcements')
	created_by = models.ForeignKey('authentication.User', on_delete=models.CASCADE, related_name='announcements')
