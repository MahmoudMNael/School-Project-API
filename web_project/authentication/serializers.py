from operator import is_
from rest_framework import serializers
from authentication.models import User

class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['id', 'full_name', 'email', 'password', 'role', 'is_pending']
		extra_kwargs = {
			'password': {'write_only': True},
		}

	def create(self, validated_data):
		password = validated_data.pop('password', None)
		is_pending = True
		instance = self.Meta.model(**validated_data)

		if instance.role == 'admin' and self.Meta.model.objects.filter(role='admin').all().count() == 0:
			is_pending = False

		if password is not None:
			instance.set_password(password)
		
		instance.is_pending = is_pending
		instance.save()
		return instance
		