import django_filters

from .models import Notice


class NoticeFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(
        field_name="category__title",
        lookup_expr="icontains",
        help_text="Filter by notice category",
    )
    priority = django_filters.ChoiceFilter(
        choices=Notice.Priority.choices, help_text="Filter by priority level"
    )
    search = django_filters.CharFilter(
        field_name="title",
        lookup_expr="icontains",
        help_text="Search by notice title",
    )

    class Meta:
        model = Notice
        fields = ["category", "priority", "search"]
