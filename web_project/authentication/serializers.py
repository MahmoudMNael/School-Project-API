from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'full_name', 'email', 'password', 'role', 'is_pending']
		extra_kwargs = {
			'password': {'write_only': True},
			'is_pending': {'read_only': True},
		}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		instance = self.Meta.model(**validated_data)
		if password is not None:
			instance.set_password(password)
		instance.save()
		return instance
		