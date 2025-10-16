from rest_framework.generics import ListAPIView, RetrieveAPIView

from .models import Committee
from .serializers import CommitteeSerializer


class CommitteeListView(ListAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Committee.objects.all().prefetch_related("panels")
    serializer_class = CommitteeSerializer


class CommitteeDetailView(RetrieveAPIView):
    authentication_classes = []
    permission_classes = []
    queryset = Committee.objects.all().prefetch_related("panels")
    serializer_class = CommitteeSerializer
