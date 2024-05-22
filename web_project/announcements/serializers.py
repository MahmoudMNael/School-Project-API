from rest_framework import serializers
from announcements.models import Announcement
from authentication.serializers import UserSerializer

class AnnouncementSerializer(serializers.ModelSerializer):
		created_by = UserSerializer(read_only=True)
		class Meta:
			model = Announcement
			fields = ['id', 'title', 'content', 'created_at', 'created_by']