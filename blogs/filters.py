from django.db.models import Q
from django_filters import CharFilter, FilterSet

from .models import Blog


class BlogFilter(FilterSet):
    category = CharFilter(field_name="category__slug", lookup_expr="icontains")
    search = CharFilter(field_name="content", method="filter_by_search")
    author = CharFilter(method="filter_by_author")

    class Meta:
        model = Blog
        fields = ["category", "search", "author"]

    def filter_by_search(self, queryset, name, value):
        return queryset.filter(
            Q(content__icontains=value)
            | Q(title__icontains=value)
            | Q(short_description__icontains=value)
            | Q(tags__icontains=value)
        )

    def filter_by_author(self, queryset, name, value):
        return queryset.filter(author__first_name__icontains=value) | queryset.filter(
            author__last_name__icontains=value
        )
