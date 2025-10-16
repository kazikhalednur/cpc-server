from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny

from .filters import AchievementFilter
from .models import Achievement
from .serializers import AchievementDetailSerializer, AchievementListSerializer


class AchievementPagination(PageNumberPagination):
    """Custom pagination for achievements list"""

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 50


class AchievementListAPIView(generics.ListAPIView):
    """
    API endpoint for listing published achievements with pagination
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = AchievementListSerializer
    pagination_class = AchievementPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = AchievementFilter

    def get_queryset(self):
        return (
            Achievement.objects.published()
            .order_by("-date", "-created_at")
            .only("id", "title", "team_name", "rank", "image", "date")
        )


class AchievementDetailAPIView(generics.RetrieveAPIView):
    """
    API endpoint for retrieving a single achievement by id (UUID)
    """

    permission_classes = [AllowAny]
    authentication_classes = []
    serializer_class = AchievementDetailSerializer
    lookup_field = "pk"

    def get_queryset(self):
        return Achievement.objects.published()
