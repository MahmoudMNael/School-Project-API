from middlewares.authentication import is_logged_in, is_admin, is_teacher
from tasks.models import Task
from authentication.models import User
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers import UserSerializer

# Create your views here.
class TaskListView(APIView):
	def get(self, request):
		current_user = is_logged_in(request)
		if current_user.role == "admin":
			tasks = Task.objects.all()
		elif current_user.role == "teacher":
			tasks = Task.objects.filter(teacher=current_user).order_by('-created_at').all()
		else:
			raise exceptions.PermissionDenied()

		tasks_data = []

		for task in tasks:
			tasks_data.append({
				'id': task.id,
				'title': task.title,
				'description': task.description,
				'priority': task.priority,
				'is_done': task.is_done,
				'created_at': task.created_at,
				'teacher': UserSerializer(task.teacher).data,
			})

		return Response(tasks_data, status=status.HTTP_200_OK)

	def post(self, request):
		current_user = is_logged_in(request)
		if current_user.role != "admin":
			raise exceptions.PermissionDenied()

		try:
			title = request.data['title']
			description = request.data['description']
			priority = request.data['priority']
			teacher_id = request.data['teacher_id']
			teacher = User.objects.filter(id=teacher_id).first()

			if teacher.role != "teacher":
				raise exceptions.ValidationError()

			task = Task(title=title, description=description, priority=priority, teacher=teacher)
			task.save()
		except:
			raise exceptions.ValidationError()

		return Response({
			'id': task.id,
			'title': task.title,
			'description': task.description,
			'priority': task.priority,
			'is_done': task.is_done,
			'created_at': task.created_at,
			'teacher': UserSerializer(task.teacher).data,
		}, status=status.HTTP_201_CREATED)

class TaskDetailView(APIView):
	def get(self, request, task_id):
		current_user = is_logged_in(request)
		task = Task.objects.filter(id=task_id).first()
		if task is None:
			raise exceptions.NotFound()

		if current_user.role == "admin" or current_user == task.teacher:
			return Response({
				'id': task.id,
				'title': task.title,
				'description': task.description,
				'priority': task.priority,
				'is_done': task.is_done,
				'created_at': task.created_at,
				'teacher': UserSerializer(task.teacher).data,
			}, status=status.HTTP_200_OK)
		else:
			raise exceptions.PermissionDenied()

	def put(self, request, task_id):
		current_user = is_admin(request)
		task = Task.objects.filter(id=task_id).first()
		if task is None:
			raise exceptions.NotFound()

		try:
			title = request.data['title']
			description = request.data['description']
			priority = request.data['priority']
			is_done = request.data['is_done']
			teacher_id = request.data['teacher_id']
			teacher = User.objects.filter(id=teacher_id).first()

			if teacher.role != "teacher":
				raise exceptions.ValidationError()

			task.title = title
			task.description = description
			task.priority = priority
			task.is_done = is_done
			task.teacher = teacher
			task.save()
		except:
			raise exceptions.ValidationError()

		return Response({
			'id': task.id,
			'title': task.title,
			'description': task.description,
			'priority': task.priority,
			'is_done': task.is_done,
			'created_at': task.created_at,
			'teacher': UserSerializer(task.teacher).data,
		}, status=status.HTTP_200_OK)

	def delete(self, request, task_id):
		current_user = is_admin(request)
		task = Task.objects.filter(id=task_id).first()
		if task is None:
			raise exceptions.NotFound()

		task.delete()
		return Response(status=status.HTTP_200_OK)

	def patch(self, request, task_id):
		current_user = is_teacher(request)
		task = Task.objects.filter(id=task_id).first()
		if task is None:
			raise exceptions.NotFound()

		try:
			is_done = request.data['is_done']
			task.is_done = is_done
			task.save()
		except:
			raise exceptions.ValidationError()

		return Response({
			'id': task.id,
			'title': task.title,
			'description': task.description,
			'priority': task.priority,
			'is_done': task.is_done,
			'created_at': task.created_at,
			'teacher': UserSerializer(task.teacher).data,
		}, status=status.HTTP_200_OK)