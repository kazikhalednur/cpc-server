from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from .filters import ContestFilter
from .models import Contest
from .serializers import ContestListSerializer, ContestSerializer


class StandardResultsSetPagination(PageNumberPagination):
    """
    Standard pagination class for contest list view
    """

    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class ContestListView(ListAPIView):
    """
    List all published contests with filtering, searching, and pagination
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = ContestListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = ContestFilter

    def get_queryset(self):
        return (
            Contest.objects.published()
            .prefetch_related("prize_set")
            .order_by("-published_at")
        )


class ContestDetailView(RetrieveAPIView):
    """
    Retrieve a specific published contest with full details
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = ContestSerializer

    def get_queryset(self):
        return Contest.objects.published().prefetch_related("prize_set")
