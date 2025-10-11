from django.urls import path

from . import views

app_name = "notices"

urlpatterns = [
    # Notice endpoints
    path("", views.NoticeListView.as_view(), name="notice-list"),
    path("<uuid:pk>/", views.NoticeDetailView.as_view(), name="notice-detail"),
    # Category and Tag endpoints
    path("categories/", views.NoticeCategoryListView.as_view(), name="category-list"),
]
