from yaml import serialize
from middlewares.authentication import is_logged_in
from authentication.models import User
from rest_framework import exceptions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from authentication.serializers import UserSerializer

class UserList(APIView):
	def get(self, request, user_type):
		current_user = is_logged_in(request)

		users = User.objects.filter(role=user_type)

		if not users:
			return Response({'message': 'No users found'}, status=status.HTTP_404_NOT_FOUND)

		serializer = UserSerializer(users, many=True)

		return Response(serializer.data, status=status.HTTP_200_OK)