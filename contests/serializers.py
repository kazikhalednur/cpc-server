from rest_framework import serializers

from .models import Contest, Prize


class PrizeSerializer(serializers.ModelSerializer):
    """
    Serializer for Prize model
    """

    class Meta:
        model = Prize
        fields = ["id", "title", "amount"]


class ContestSerializer(serializers.ModelSerializer):
    """
    Full serializer for Contest detail view with all fields and related prizes
    """

    difficulty_level = serializers.CharField(source="get_difficulty_level_display")
    status = serializers.CharField(source="get_status_display")
    prizes = PrizeSerializer(source="prize_set", many=True, read_only=True)

    class Meta:
        model = Contest
        fields = [
            "id",
            "title",
            "image",
            "short_description",
            "description",
            "start_time",
            "end_time",
            "difficulty_level",
            "platform",
            "platform_link",
            "participants",
            "max_participants",
            "registration_link",
            "registration_deadline",
            "organizer",
            "status",
            "prizes",
            "created_at",
            "updated_at",
            "published_at",
        ]


class ContestListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for Contest list view
    """

    difficulty_level = serializers.CharField(source="get_difficulty_level_display")
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Contest
        fields = [
            "id",
            "title",
            "image",
            "short_description",
            "start_time",
            "end_time",
            "difficulty_level",
            "platform",
            "participants",
            "status",
            "published_at",
        ]
