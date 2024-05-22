from authentication.models import User
from rest_framework import exceptions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from authentication.serializers import UserSerializer
from middlewares.authentication import is_logged_in, is_admin
import jwt, datetime


class LoginView(APIView):
	def post(self, request):
		email = request.data.get('email')
		password = request.data.get('password')

		user = User.objects.filter(email=email).first()

		if not user:
			raise exceptions.AuthenticationFailed('User not found')
		
		if not user.check_password(password):
			raise exceptions.AuthenticationFailed('Incorrect password')
		
		if user.is_pending:
			return Response({'message': 'User is pending approval'}, status=status.HTTP_204_NO_CONTENT)
		
		payload = {
			'id': user.id,
			'exp': datetime.datetime.utcnow() + datetime.timedelta(days=1),
			'iat': datetime.datetime.utcnow()
		}

		token = jwt.encode(payload, 'secret', algorithm='HS256')

		response = Response()
		response.set_cookie(key='jwt', value=token, httponly=True)
		response.data = {
			'message': 'User logged in'
		}
		response.status_code = status.HTTP_200_OK

		return response

	

class RegisterView(APIView):
	def post(self, request):
		serializer = UserSerializer(data=request.data)
		serializer.is_valid(raise_exception=True)
		serializer.save()

		if serializer.data['is_pending'] == True:
			return Response({'message': 'User created and pending approval'}, status=status.HTTP_201_CREATED)
		
		return Response({'message': 'User created'}, status=status.HTTP_201_CREATED)



class PendingUsersView(APIView):
	def get(self, request):
		current_user = is_admin(request)

		pending_users = User.objects.filter(is_pending=True).order_by('date_joined')

		serialized_users = UserSerializer(pending_users, many=True)

		pending_teachers_count = User.objects.filter(is_pending=True, role='teacher').count()

		pending_admins_count = User.objects.filter(is_pending=True, role='admin').count()

		pending_students_count = User.objects.filter(is_pending=True, role='student').count()

		return Response({'data': serialized_users.data, 'admins_count': pending_admins_count, 'teachers_count': pending_teachers_count, 'students_count': pending_students_count,}, status=status.HTTP_200_OK)
	


class ApproveUserView(APIView):
	def post(self, request, user_id):
		current_user = is_admin(request)
		
		user_to_approve = User.objects.filter(id=user_id).first()

		if not user_to_approve:
			raise exceptions.NotFound('User not found')
		
		user_to_approve.is_pending = False
		user_to_approve.save()

		return Response({'message': 'User approved'}, status=status.HTTP_200_OK)
	
	def delete(self, request, user_id):
		current_user = is_admin(request)
		
		user_to_delete = User.objects.filter(id=user_id).first()

		if not user_to_delete:
			raise exceptions.NotFound('User not found')
		
		user_to_delete.delete()

		return Response({'message': 'User deleted'}, status=status.HTTP_200_OK)

	
class ProfileView(APIView):
	def get(self, request):
		user = is_logged_in(request)

		serializer = UserSerializer(user)

		return Response(serializer.data, status=status.HTTP_200_OK)
	