from rest_framework import serializers

from ..helpers import (
    get_student_data,
    match_email_domain,
    split_name_equal,
)
from ..models import User


class SignupSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(max_length=128, write_only=True)

    class Meta:
        model = User
        fields = [
            "email",
            "student_id",
            "password",
            "password2",
        ]

    def validate(self, attrs):
        if not match_email_domain(attrs["email"]):
            raise serializers.ValidationError(
                {"email": "Try with your DIU email address"}
            )

        if not get_student_data(attrs["student_id"]):
            raise serializers.ValidationError({"student_id": "Invalid student ID"})

        if attrs["password"] != attrs["password2"]:
            raise serializers.ValidationError({"password": "Password doesn't matched"})
        attrs.pop("password2")

        return attrs

    def save(self, **kwargs):
        student_id = self.validated_data["student_id"]
        student_data = get_student_data(student_id)

        user = User.objects.create_user(
            email=self.validated_data["email"],
            password=self.validated_data["password"],
            first_name=split_name_equal(student_data["studentName"])["first_name"],
            last_name=split_name_equal(student_data["studentName"])["last_name"],
            student_id=student_id,
            batch_no=student_data["batchNo"],
            batch_inital=student_data["semesterId"],
            department=student_data["deptShortName"],
        )

        return user
