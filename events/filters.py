import django_filters
from django.utils import timezone

from .models import Event


class EventFilter(django_filters.FilterSet):
    status = django_filters.ChoiceFilter(
        choices=[
            ("UPCOMING", "Upcoming"),
            ("ONGOING", "Ongoing"),
            ("COMPLETED", "Completed"),
        ],
        help_text="Filter by event status",
        method="filter_by_status",
    )
    wing = django_filters.CharFilter(
        field_name="wing__title",
        lookup_expr="icontains",
        help_text="Filter by wing name",
    )
    search = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", help_text="Search by event title"
    )

    def filter_by_status(self, queryset, name, value):
        if value == "UPCOMING":
            return queryset.filter(event_date__gte=timezone.now())
        elif value == "ONGOING":
            return queryset.filter(
                event_date__lte=timezone.now(),
                registration_deadline__gte=timezone.now(),
            )
        elif value == "COMPLETED":
            return queryset.filter(registration_deadline__lt=timezone.now())

    class Meta:
        model = Event
        fields = ["status", "wing", "search"]
