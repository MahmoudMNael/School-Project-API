from django.urls import include, path

from announcements.views import AnnouncementsListView, AnnouncementDetailView

urlpatterns = [
	path('', AnnouncementsListView.as_view(), name='announcements_list'),
	path('<int:announcement_id>/', AnnouncementDetailView.as_view(), name='announcement_detail'),
]