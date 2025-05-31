from rest_framework import serializers

from ..models import User


class UserInfoSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(read_only=True)

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "picture",
            "phone_number",
        ]
