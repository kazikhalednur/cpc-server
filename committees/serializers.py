from rest_framework import serializers

from .models import Committee, Panel


class PanelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Panel
        fields = ["id", "type", "image"]


class CommitteeSerializer(serializers.ModelSerializer):
    panels = PanelSerializer(many=True, read_only=True)

    class Meta:
        model = Committee
        fields = ["id", "year", "panels"]
