import jwt
from rest_framework import exceptions
from authentication.models import User

def is_logged_in(request):
	token = request.COOKIES.get('jwt')

	if not token:
		raise exceptions.AuthenticationFailed('Unauthenticated')
		
	try:
		payload = jwt.decode(token, 'secret', algorithms=['HS256'])
	except jwt.ExpiredSignatureError:
		raise exceptions.AuthenticationFailed('Unauthenticated')
		
	user = User.objects.filter(id=payload['id']).first()

	return user

def is_admin(request):
	user = is_logged_in(request)

	if user.role != 'admin':
		raise exceptions.PermissionDenied('Unauthorized')

	return user

def is_teacher(request):
	user = is_logged_in(request)

	if user.role != 'teacher':
		raise exceptions.PermissionDenied('Unauthorized')

	return user

def is_student(request):
	user = is_logged_in(request)

	if user.role != 'student':
		raise exceptions.PermissionDenied('Unauthorized')

	return user