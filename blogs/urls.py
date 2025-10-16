from django.urls import path

from . import views

app_name = "blogs"

urlpatterns = [
    path(
        "categories/",
        views.BlogCategoryListAPIView.as_view(),
        name="blog-category-list",
    ),
    path(
        "<str:slug>/like/",
        views.BlogLikeToggleAPIView.as_view(),
        name="blog-like-toggle",
    ),
    path(
        "<str:slug>/bookmark/",
        views.BlogBookmarkToggleAPIView.as_view(),
        name="blog-bookmark-toggle",
    ),
    path("<str:slug>/", views.BlogDetailAPIView.as_view(), name="blog-detail"),
    path("", views.BlogListAPIView.as_view(), name="blog-list"),
]
