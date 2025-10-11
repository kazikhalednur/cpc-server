from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from .filters import NoticeFilter
from .models import Notice, NoticeCategory
from .serializers import NoticeCategorySerializer, NoticeSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class NoticeListView(ListAPIView):
    """
    List all published notices with filtering and pagination
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = NoticeSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = NoticeFilter

    def get_queryset(self):
        return (
            Notice.objects.published()
            .select_related("category")
            .prefetch_related("tags")
            .order_by("-is_pinned", "-published_at")
        )


class NoticeDetailView(RetrieveAPIView):
    """
    Retrieve a specific published notice
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = NoticeSerializer

    def get_queryset(self):
        return (
            Notice.objects.published()
            .select_related("category")
            .prefetch_related("tags")
        )


class NoticeCategoryListView(ListAPIView):
    """
    List all notice categories
    """

    authentication_classes = []
    permission_classes = []
    queryset = NoticeCategory.objects.all()
    serializer_class = NoticeCategorySerializer
