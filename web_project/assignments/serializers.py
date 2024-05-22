from rest_framework import serializers
from assignments.models import Assignment
from authentication.serializers import UserSerializer

class AssignmentSerializer(serializers.ModelSerializer):
	created_by = UserSerializer(read_only=True)
	class Meta:
		model = Assignment
		fields = ['id', 'title', 'content', 'due_date', 'created_at', 'created_by']


class CommentSerializer(serializers.ModelSerializer):
	created_by = UserSerializer(read_only=True)
	class Meta:
		model = Assignment
		fields = ['id', 'content', 'created_at', 'created_by']


class SubmissionSerializer(serializers.ModelSerializer):
	created_by = UserSerializer(read_only=True)
	class Meta:
		model = Assignment
		fields = ['id', 'link', 'created_at', 'created_by']