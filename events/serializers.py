from rest_framework import serializers

from committees.models import Wing

from .models import Event, EventGuest, EventSpeaker


class WingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wing
        fields = ["title", "short_title"]


class EventSpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventSpeaker
        fields = ["id", "name", "designation", "organization", "country"]


class EventGuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventGuest
        fields = ["id", "name", "designation", "organization", "country"]


class EventSerializer(serializers.ModelSerializer):
    wing = serializers.CharField(source="wing.title")
    speakers = EventSpeakerSerializer(many=True, read_only=True)
    guests = EventGuestSerializer(many=True, read_only=True)
    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Event
        fields = [
            "id",
            "wing",
            "title",
            "short_description",
            "description",
            "image",
            "speakers",
            "guests",
            "event_date",
            "registration_deadline",
            "registration_link",
            "venue",
            "status",
            "published_at",
        ]


class EventListSerializer(serializers.ModelSerializer):
    """
    Simplified serializer for event list view
    """

    status = serializers.CharField(source="get_status_display")

    class Meta:
        model = Event
        fields = [
            "id",
            "title",
            "image",
            "event_date",
            "short_description",
            "registration_deadline",
            "venue",
            "status",
        ]
