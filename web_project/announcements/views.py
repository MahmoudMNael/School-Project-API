from middlewares.authentication import is_logged_in, is_teacher
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from classrooms.models import Classroom
from announcements.serializers import AnnouncementSerializer
from announcements.models import Announcement

class AnnouncementsListView(APIView):
	def get(self, request, classroom_id):
		current_user = is_logged_in(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()

		if not classroom:
			raise exceptions.NotFound('Classroom not found')

		if current_user.role == 'admin' or classroom.teacher == current_user or current_user in classroom.students.all():
			announcements = classroom.announcements.order_by('-created_at').all()
			serialized_announcements = AnnouncementSerializer(announcements, many=True)
			return Response(serialized_announcements.data, status=status.HTTP_200_OK)
		else:
			raise exceptions.PermissionDenied('You do not have permission to view this classroom')

	def post(self, request, classroom_id):
		current_user = is_teacher(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()

		if not classroom:
			raise exceptions.NotFound('Classroom not found')

		if classroom.teacher != current_user:
			raise exceptions.PermissionDenied('You do not have permission to create an announcement for this classroom')

		title = request.data.get('title')
		content = request.data.get('content')

		try:
			announcement = Announcement(title=title, content=content, classroom=classroom, created_by=current_user)
			announcement.save()
			serializer = AnnouncementSerializer(announcement)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		except:
			raise exceptions.ValidationError('An error occurred while creating the announcement')
		


class AnnouncementDetailView(APIView):
	def get(self, request, classroom_id, announcement_id):
		current_user = is_logged_in(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()
		announcement = Announcement.objects.filter(id=announcement_id).first()

		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if not announcement:
			raise exceptions.NotFound('Announcement not found')
		
		if current_user.role == 'admin' or classroom.teacher == current_user or current_user in classroom.students.all():
			serializer = AnnouncementSerializer(announcement)
			return Response(serializer.data, status=status.HTTP_200_OK)
		else:
			raise exceptions.PermissionDenied('You do not have permission to view this announcement')
		
	def put(self, request, classroom_id, announcement_id):
		current_user = is_teacher(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()
		announcement = Announcement.objects.filter(id=announcement_id).first()

		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if not announcement:
			raise exceptions.NotFound('Announcement not found')
		
		if classroom.teacher != current_user:
			raise exceptions.PermissionDenied('You do not have permission to update this announcement')
		
		title = request.data.get('title')
		content = request.data.get('content')

		try:
			announcement.title = title
			announcement.content = content
			announcement.save()
			serializer = AnnouncementSerializer(announcement)
			return Response(serializer.data, status=status.HTTP_200_OK)
		except:
			raise exceptions.ValidationError('An error occurred while updating the announcement')
		
	def delete(self, request, classroom_id, announcement_id):
		current_user = is_teacher(request)
		classroom = Classroom.objects.filter(id=classroom_id).first()
		announcement = Announcement.objects.filter(id=announcement_id).first()

		if not classroom:
			raise exceptions.NotFound('Classroom not found')
		
		if not announcement:
			raise exceptions.NotFound('Announcement not found')
		
		if classroom.teacher != current_user:
			raise exceptions.PermissionDenied('You do not have permission to delete this announcement')
		
		announcement.delete()
		return Response(status=status.HTTP_200_OK)