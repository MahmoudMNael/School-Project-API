from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
		path('api/auth/', include('authentication.urls')),
		path('api/tasks/', include('tasks.urls')),
		path('api/users/', include('users.urls')),
		path('api/classrooms/', include('classrooms.urls')),
		path('api/classrooms/<int:classroom_id>/assignments/', include('assignments.urls')),
		path('api/classrooms/<int:classroom_id>/announcements/', include('announcements.urls')),
]
