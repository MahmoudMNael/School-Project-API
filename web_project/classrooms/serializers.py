from asyncore import read
from rest_framework import serializers
from classrooms.models import Classroom
from authentication.serializers import UserSerializer

class ClassroomSerializer(serializers.ModelSerializer):
	teacher = UserSerializer(read_only=True)
	class Meta:
		model = Classroom
		fields = ['id', 'name', 'teacher']