from django.urls import path

from .views import CommitteeDetailView, CommitteeListView

urlpatterns = [
    path("", CommitteeListView.as_view(), name="committee-list"),
    path("<uuid:pk>/", CommitteeDetailView.as_view(), name="committee-detail"),
]
