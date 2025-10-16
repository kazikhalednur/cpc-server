from django.urls import path

from . import views

app_name = "achievements"

urlpatterns = [
    path("", views.AchievementListAPIView.as_view(), name="achievement-list"),
    path(
        "<uuid:pk>/",
        views.AchievementDetailAPIView.as_view(),
        name="achievement-detail",
    ),
]
