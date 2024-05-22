from django.urls import include, path
from tasks.views import TaskListView, TaskDetailView

urlpatterns = [
	path('', TaskListView.as_view(), name='task_list'),
	path('<int:task_id>/', TaskDetailView.as_view(), name='task_detail'),
]