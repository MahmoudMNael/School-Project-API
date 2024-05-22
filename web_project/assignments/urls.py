from django.urls import include, path

from assignments.views import AssignmentsListView

urlpatterns = [
	path('', AssignmentsListView.as_view(), name='assignments_list'),
	# path('<int:assignment_id/', AssignmentDetailView.as_view(), name='assignment_detail'),
	# path('<int:assignment_id>/comments/', CommentsListView.as_view(), name='comments_list'),
	# path('<int:assignment_id>/comments/<int:comment_id>/', CommentActionView.as_view(), name='comment_action'),
	# path('<int:assignment_id>/submissions/', SubmissionsListView.as_view(), name='submissions_list'),
	# path('<int:assignment_id>/submissions/<int:submission_id>/', SubmissionActionView.as_view(), name='submission_action'),
]