from django.db.models import Q
from django_filters import CharFilter, FilterSet

from .models import Achievement


class AchievementFilter(FilterSet):
    search = CharFilter(method="filter_by_search")

    class Meta:
        model = Achievement
        fields = ["search"]

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(title__icontains=value)
            | Q(team_name__icontains=value)
            | Q(rank__icontains=value)
        )
