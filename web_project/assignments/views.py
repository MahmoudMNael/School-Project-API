from middlewares.authentication import is_logged_in, is_teacher
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from classrooms.models import Classroom
from assignments.serializers import AssignmentSerializer, CommentSerializer, SubmissionSerializer
from assignments.models import Assignment, Comment, Submission

class AssignmentsListView(APIView):
	def get(self, request, classroom_id):
		current_user = is_logged_in(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()

		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if current_user.role == 'admin' or classroom.teacher == current_user or current_user in classroom.students.all():
			assignments = classroom.assignments.order_by('-created_at').all()
			serialized_assignments = AssignmentSerializer(assignments, many=True)
			return Response(serialized_assignments.data, status=status.HTTP_200_OK)
		else:
			raise exceptions.PermissionDenied('You do not have permission to view this classroom')
		
	def post(self, request, classroom_id):
		current_user = is_teacher(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()

		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if classroom.teacher != current_user:
			raise exceptions.PermissionDenied('You do not have permission to create an assignment for this classroom')
		
		title = request.data.get('title')
		content = request.data.get('content')
		due_date = request.data.get('due_date')

		try:
			assignment = Assignment(title=title, content=content, due_date=due_date, classroom=classroom, created_by=current_user)
			assignment.save()
			serializer = AssignmentSerializer(assignment)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except:
			raise exceptions.ValidationError('An error occurred while creating the assignment')
