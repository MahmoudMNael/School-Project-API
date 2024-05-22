from django.urls import path
from authentication import views

urlpatterns = [
	path('login/', views.LoginView.as_view(), name='login_view'),
	path('register/', views.RegisterView.as_view(), name='register_view'),
	path('profile/', views.ProfileView.as_view(), name='profile_view'),
	path('pending/<int:user_id>/', views.ApproveUserView.as_view(), name='approve_user_view'),
	path('pending/', views.PendingUsersView.as_view(), name='pending_users_view'),
]