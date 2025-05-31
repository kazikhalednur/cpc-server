from rest_framework import serializers

from ..helpers import (
    get_student_data,
    google_user_details,
    match_email_domain,
    match_email_id_digits_group,
    split_name_equal,
)
from ..models import User


class SignupGoogleSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=500, write_only=True)
    student_id = serializers.CharField(max_length=20, write_only=True)

    def save(self, **kwargs):
        code = self.validated_data["code"]
        student_id = self.validated_data["student_id"]

        google_data = google_user_details(code)
        email = google_data["email"]

        if not match_email_domain(email):
            raise serializers.ValidationError(
                {"email": "Try with your DIU email address"}
            )

        if not get_student_data(student_id):
            raise serializers.ValidationError({"student_id": "Invalid student ID"})

        if not match_email_id_digits_group(student_id, email):
            raise serializers.ValidationError({"email": "Give your id not another id"})

        student_data = get_student_data(student_id)

        user = User.objects.create_user(
            sub=google_data["sub"],
            is_google_login=True,
            email=email,
            email_verified=google_data["email_verified"],
            password=google_data["sub"],
            picture=google_data["picture"],
            first_name=split_name_equal(student_data["studentName"])["first_name"],
            last_name=split_name_equal(student_data["studentName"])["last_name"],
            student_id=student_id,
            batch_no=student_data["batchNo"],
            batch_inital=student_data["semesterId"],
            department=student_data["deptShortName"],
        )

        return user
