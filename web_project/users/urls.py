from django.urls import include, path
from users.views import UserList

urlpatterns = [
    path('<str:user_type>/', UserList.as_view(), name='user_list'),
]