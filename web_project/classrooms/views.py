from middlewares.authentication import is_admin, is_logged_in, is_student
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from classrooms.models import Classroom
from classrooms.serializers import ClassroomSerializer
from authentication.models import User
from authentication.serializers import UserSerializer

class ClassroomListView(APIView):
		def get(self, request):
			current_user = is_logged_in(request)
			if current_user.role == 'admin':
				classrooms = Classroom.objects.all()
			elif current_user.role == 'teacher':
				classrooms = current_user.classrooms_monitored.all()
			else:
				classrooms = current_user.classrooms_joined.all()

			if not classrooms:
				raise exceptions.NotFound('No classrooms found')
			
			serializer = ClassroomSerializer(classrooms, many=True)

			return Response(serializer.data, status=status.HTTP_200_OK)
		
		def post(self, request):
			current_user = is_admin(request)
			name = request.data['name']
			teacher_id = request.data['teacher_id']
			teacher = User.objects.filter(id=teacher_id).first()
			if not teacher:
				raise exceptions.ValidationError('Teacher not found')
			
			try:
				classroom = Classroom(name=name, teacher=teacher)
				classroom.save()
			except Exception as e:
				raise exceptions.ValidationError(str(e))
			
			serializer = ClassroomSerializer(classroom)
			return Response(serializer.data, status=status.HTTP_201_CREATED)


class ClassroomDetailsView(APIView):
	def get(self, request, classroom_id):
		current_user = is_logged_in(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()
		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if current_user.role == 'admin' or current_user == classroom.teacher or current_user in classroom.students.all():
			serializer = ClassroomSerializer(classroom)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			raise exceptions.PermissionDenied('You do not have permission to view this classroom')
	

class ClassroomJoinView(APIView):
	def post(self, request, classroom_id):
		current_user = is_student(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()
		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if current_user in classroom.students.all():
			raise exceptions.ValidationError('You have already joined this classroom')
		
		classroom.students.add(current_user)
		classroom.save()

		serializer = ClassroomSerializer(classroom)
		return Response(serializer.data, status=status.HTTP_200_OK)
	

class ClassroomPeopleView(APIView):
	def get(self, request, classroom_id):
		current_user = is_logged_in(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()
		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if current_user.role == 'admin' or current_user == classroom.teacher or current_user in classroom.students.all():
			teacher = UserSerializer(classroom.teacher)
			students = UserSerializer(classroom.students.order_by('full_name'), many=True)
			return Response({'teacher': teacher.data, 'students': students.data}, status=status.HTTP_200_OK)
		else:
			raise exceptions.PermissionDenied('You do not have permission to view this classroom')