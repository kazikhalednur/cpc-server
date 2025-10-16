import django_filters
from django.utils import timezone

from .models import Contest


class ContestFilter(django_filters.FilterSet):
    """
    Filter set for Contest list view with search and filtering capabilities
    """

    difficulty_level = django_filters.ChoiceFilter(
        choices=Contest.DifficultyLevel.choices,
        help_text="Filter by difficulty level",
    )
    platform = django_filters.CharFilter(
        field_name="platform",
        lookup_expr="icontains",
        help_text="Filter by platform name",
    )
    search = django_filters.CharFilter(
        field_name="title", lookup_expr="icontains", help_text="Search by contest title"
    )
    status = django_filters.CharFilter(
        help_text="Filter by contest status",
        method="filter_by_status",
    )
    start_time_from = django_filters.DateTimeFilter(
        field_name="start_time",
        lookup_expr="gte",
        help_text="Filter contests starting from this date/time",
    )
    start_time_to = django_filters.DateTimeFilter(
        field_name="start_time",
        lookup_expr="lte",
        help_text="Filter contests starting up to this date/time",
    )
    end_time_from = django_filters.DateTimeFilter(
        field_name="end_time",
        lookup_expr="gte",
        help_text="Filter contests ending from this date/time",
    )
    end_time_to = django_filters.DateTimeFilter(
        field_name="end_time",
        lookup_expr="lte",
        help_text="Filter contests ending up to this date/time",
    )

    class Meta:
        model = Contest
        fields = [
            "difficulty_level",
            "platform",
            "search",
            "status",
            "start_time_from",
            "start_time_to",
            "end_time_from",
            "end_time_to",
        ]

    def filter_by_status(self, queryset, name, value):
        if value == "UPCOMING":
            return queryset.filter(start_time__gte=timezone.now())
        elif value == "ONGOING":
            return queryset.filter(
                start_time__lte=timezone.now(), end_time__gte=timezone.now()
            )
        elif value == "COMPLETED":
            return queryset.filter(end_time__lte=timezone.now())
