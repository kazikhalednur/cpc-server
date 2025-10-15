from django.urls import path

from .views import ContestDetailView, ContestListView

app_name = "contests"

urlpatterns = [
    path("", ContestListView.as_view(), name="contest-list"),
    path("<uuid:pk>/", ContestDetailView.as_view(), name="contest-detail"),
]
