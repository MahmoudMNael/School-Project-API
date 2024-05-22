from django.contrib import admin
from assignments.models import Assignment, Comment, Submission

# Register your models here.
admin.site.register(Assignment)
admin.site.register(Comment)
admin.site.register(Submission)