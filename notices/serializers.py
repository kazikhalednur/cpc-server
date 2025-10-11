from drf_spectacular.utils import extend_schema_field
from rest_framework import serializers

from .models import Notice, NoticeCategory


class NoticeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = NoticeCategory
        fields = ["title"]


class NoticeSerializer(serializers.ModelSerializer):
    category = serializers.CharField(source="category.title")
    tags = serializers.SerializerMethodField()

    class Meta:
        model = Notice
        fields = [
            "id",
            "title",
            "content",
            "category",
            "priority",
            "tags",
            "is_pinned",
            "status",
            "published_at",
            "updated_at",
        ]

    @extend_schema_field(serializers.ListField(child=serializers.CharField()))
    def get_tags(self, obj):
        return obj.tags.values_list("title", flat=True)
