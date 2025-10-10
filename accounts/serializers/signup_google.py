from rest_framework import serializers
from rest_framework_simplejwt.tokens import RefreshToken

from ..helpers import (  # get_student_data,
    google_user_details,
    match_email_domain,
    match_email_id_digits_group,
    split_name_equal,
)
from ..models import User


class SignupGoogleSerializer(serializers.Serializer):
    token_class = RefreshToken

    code = serializers.CharField(max_length=500, write_only=True)
    student_id = serializers.CharField(max_length=20, write_only=True)
    refresh = serializers.CharField(max_length=500, read_only=True)
    access = serializers.CharField(max_length=500, read_only=True)

    def save(self, **kwargs):
        code = self.validated_data["code"]
        student_id = self.validated_data["student_id"]

        google_data = google_user_details(code, 0)
        email = google_data["email"]

        if not match_email_domain(email):
            raise serializers.ValidationError(
                {"email": "Try with your DIU email address"}
            )

        if not match_email_id_digits_group(student_id, email):
            raise serializers.ValidationError({"email": "Give your id not another id"})

        if User.objects.filter(student_id=student_id, email=email).exists():
            user = User.objects.get(student_id=student_id, email=email)
            refresh = self.token_class.for_user(user)
            self.validated_data["refresh"] = str(refresh)
            self.validated_data["access"] = str(refresh.access_token)

            return user

        user = User.objects.create_user(
            sub=google_data["sub"],
            is_google_login=True,
            email=email,
            email_verified=google_data["email_verified"],
            password=google_data["sub"],
            picture=google_data["picture"],
            first_name=split_name_equal(google_data["name"])["first_name"],
            last_name=split_name_equal(google_data["name"])["last_name"],
            student_id=student_id,
        )
        user.set_unusable_password()
        user.save()

        refresh = self.token_class.for_user(user)
        self.validated_data["refresh"] = str(refresh)
        self.validated_data["access"] = str(refresh.access_token)

        return user
