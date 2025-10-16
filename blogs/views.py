from django.db.models import F
from django_filters.rest_framework import DjangoFilterBackend
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import generics, permissions
from rest_framework import serializers as drf_serializers
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import BlogFilter
from .models import Blog, BlogBookmark, BlogCategory, BlogLike
from .serializers import (
    BlogCategorySerializer,
    BlogDetailSerializer,
    BlogListSerializer,
)


class BlogPagination(PageNumberPagination):
    """Custom pagination for blog list"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class BlogListAPIView(generics.ListAPIView):
    """
    API endpoint for listing published blogs with pagination and filtering
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = BlogListSerializer
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = BlogFilter

    def get_queryset(self):
        """Return only published blogs for public access"""
        return (
            Blog.objects.published()
            .select_related("category", "author")
            .prefetch_related("likes", "bookmarks")
            .order_by("-published_at")
        )


class BlogDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single blog by slug
    """

    permission_classes = [AllowAny]
    serializer_class = BlogDetailSerializer
    lookup_field = "slug"

    def get_queryset(self):
        """Return only published blogs for public access"""
        return (
            Blog.objects.published()
            .select_related("category", "author")
            .prefetch_related("likes", "bookmarks")
            .order_by("-published_at")
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["request"] = self.request
        return context

    def retrieve(self, request, *args, **kwargs):
        """Override retrieve to increment views_count on each access"""
        instance = self.get_object()

        # Increment views count
        Blog.objects.filter(pk=instance.pk).update(views_count=F("views_count") + 1)

        # Refresh the instance to get updated views_count
        instance.refresh_from_db()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class BlogCategoryListAPIView(generics.ListAPIView):
    """
    API endpoint for listing blog categories
    """

    queryset = BlogCategory.objects.all()
    serializer_class = BlogCategorySerializer
    permission_classes = [permissions.AllowAny]


class BlogLikeToggleAPIView(APIView):
    @extend_schema(
        summary="Toggle blog like",
        description="Toggle blog like",
        responses={
            200: inline_serializer(
                name="BlogLikeToggleAPIViewResponse",
                fields={
                    "liked": drf_serializers.BooleanField(default=True),
                    "likes": drf_serializers.IntegerField(default=0),
                },
            ),
        },
    )
    def post(self, request, slug):
        try:
            blog = Blog.objects.published().get(slug=slug)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
            )

        like, created = BlogLike.objects.get_or_create(blog=blog, user=request.user)
        if created:
            return Response({"liked": True, "likes": blog.likes.count()})
        else:
            like.delete()
            return Response({"liked": False, "likes": blog.likes.count()})


class BlogBookmarkToggleAPIView(APIView):
    @extend_schema(
        summary="Toggle blog bookmark",
        description="Toggle blog bookmark",
        responses={
            200: inline_serializer(
                name="BlogBookmarkToggleAPIViewResponse",
                fields={
                    "bookmarked": drf_serializers.BooleanField(default=True),
                    "bookmarks": drf_serializers.IntegerField(default=0),
                },
            ),
        },
    )
    def post(self, request, slug):
        try:
            blog = Blog.objects.published().get(slug=slug)
        except Blog.DoesNotExist:
            return Response(
                {"error": "Blog not found"}, status=status.HTTP_404_NOT_FOUND
            )

        bookmark, created = BlogBookmark.objects.get_or_create(
            blog=blog, user=request.user
        )
        if created:
            return Response({"bookmarked": True, "bookmarks": blog.bookmarks.count()})
        else:
            bookmark.delete()
            return Response({"bookmarked": False, "bookmarks": blog.bookmarks.count()})
