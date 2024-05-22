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


class AssignmentDetailView(APIView):
	def get(self, request, classroom_id, assignment_id):
		current_user = is_logged_in(request)
		assignment = Assignment.objects.filter(id=assignment_id).first()
		classroom = Classroom.objects.filter(id=classroom_id).first()
		serialized_assignment = AssignmentSerializer(assignment)

		return Response(serialized_assignment.data , status=status.HTTP_200_OK)
	
	def put(self, request, classroom_id, assignment_id):
		current_user = is_logged_in(request)
		assignment = Assignment.objects.filter(id=assignment_id).first()
		classroom = Classroom.objects.filter(id=classroom_id).first()

		if not assignment:
			raise exceptions.NotFound('Assignment not found')
		
		if classroom.teacher == current_user:
			title = request.data.get('title')
			content = request.data.get('content')
			due_date = request.data.get('due_date')
			try:
				assignment = Assignment(title=title, content=content, due_date=due_date, created_by=current_user, classroom=classroom)
				assignment.save()
				serialized_assignment = AssignmentSerializer(assignment)
				return Response(serialized_assignment.data, status=status.HTTP_200_OK)
			except:
				raise exceptions.ValidationError('An error occurred while editing the assignment')

		else:
			raise exceptions.PermissionDenied('You do not have permission to edit this assignment')

	def delete(self, request, classroom_id, assignment_id):
		current_user = is_logged_in(request)
		assignment = Assignment.objects.filter(id=assignment_id).first()
		classroom = Classroom.objects.filter(id=classroom_id).first()

		if not assignment:
			raise exceptions.NotFound('Assignment not found')

		if classroom.teacher == current_user:
			assignment.delete()
			return Response({"message":"This assignment is deleted successfully"},status=status.HTTP_200_OK)

		else:
			raise exceptions.PermissionDenied('You do not have permission to delete this assignment')


class CommentsListView(APIView):
	def get(self, request, classroom_id, assignment_id):
		assignment = Assignment.objects.filter(id=assignment_id).first()
		comment = assignment.comments.all()
		serialized_comments = CommentSerializer(comment , many=True)

		if not assignment:
			raise exceptions.NotFound('Assignment not found')
		
		return Response(serialized_comments.data, status=status.HTTP_200_OK)
		
	def post(self, request, classroom_id, assignment_id):
		current_user = is_logged_in(request)
		assignment = Assignment.objects.filter(id=assignment_id).first()
		classroom = Classroom.objects.filter(id=classroom_id).first()

		if not assignment:
			raise exceptions.NotFound('Assignment not found')

		if classroom.teacher == current_user or current_user in classroom.students.all():
			content = request.data.get('content')
			try:
				comment = Comment(content=content, created_by=current_user, assignment=assignment)
				comment.save()
				serialized_comment = CommentSerializer(comment)
				return Response(serialized_comment.data, status=status.HTTP_201_CREATED)
			except:
				raise exceptions.ValidationError('An error occurred while creating the comment')

		else:
			raise exceptions.PermissionDenied('You do not have permission to view this classroom')

class SubmissionsListView(APIView):
	def get(self, request, classroom_id, assignment_id):
		assignment = Assignment.objects.filter(id=assignment_id).first()
		classroom = Classroom.objects.filter(id=classroom_id).first()
		submit_links = assignment.submissions.all()
		serialized_links = SubmissionSerializer(submit_links , many=True)

		if not assignment:
			raise exceptions.NotFound('Assignment not found')
		
		return Response(serialized_links.data , status=status.HTTP_200_OK)
	
	def post(self, request, classroom_id, assignment_id):
		current_user = is_logged_in(request)
		assignment = Assignment.objects.filter(id=assignment_id).first()
		classroom = Classroom.objects.filter(id=classroom_id).first()

		
		if not assignment:
			raise exceptions.NotFound('Assignment not found')
		
		if current_user in classroom.students.all():
			link = request.data.get('link')
			try:
				submit_link = Submission(link=link, created_by=current_user, assignment=assignment)
				submit_link.save()
				serialized_link = SubmissionSerializer(submit_link)
				return Response(serialized_link.data, status=status.HTTP_201_CREATED)
			except:
				raise exceptions.ValidationError('An error occurred while creating the submission link')
		else:
			raise exceptions.PermissionDenied('You do not have permission to view this classroom')
