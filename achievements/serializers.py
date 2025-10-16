from rest_framework import serializers

from .models import Achievement


class AchievementListSerializer(serializers.ModelSerializer):
    """Serializer for achievements list view with basic information"""

    class Meta:
        model = Achievement
        fields = [
            "id",
            "title",
            "team_name",
            "rank",
            "image",
            "date",
        ]


class AchievementDetailSerializer(serializers.ModelSerializer):
    """Serializer for achievements detail view with full information"""

    class Meta:
        model = Achievement
        fields = ["id", "title", "team_name", "rank", "image", "description", "date"]
