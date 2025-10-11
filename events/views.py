from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.pagination import PageNumberPagination

from .filters import EventFilter
from .models import Event
from .serializers import EventListSerializer, EventSerializer


class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class EventListView(ListAPIView):
    """
    List all events with filtering, searching, and pagination
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = EventListSerializer
    pagination_class = StandardResultsSetPagination
    filter_backends = [DjangoFilterBackend]
    filterset_class = EventFilter

    def get_queryset(self):
        return Event.objects.published().select_related("wing")


class EventDetailView(RetrieveAPIView):
    """
    Retrieve a specific event with full details
    """

    authentication_classes = []
    permission_classes = []
    serializer_class = EventSerializer

    def get_queryset(self):
        return Event.objects.published().select_related("wing")
