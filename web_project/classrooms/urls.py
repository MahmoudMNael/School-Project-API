from django.urls import include, path
from classrooms.views import ClassroomJoinView, ClassroomListView, ClassroomDetailsView, ClassroomPeopleView

urlpatterns = [
	path('', ClassroomListView.as_view(), name='classroom_list'),
	path('<int:classroom_id>/', ClassroomDetailsView.as_view(), name='classroom_detail'),
	path('<int:classroom_id>/join/', ClassroomJoinView.as_view(), name='classroom_join'),
	path('<int:classroom_id>/people/', ClassroomPeopleView.as_view(), name='classroom_people'),
]