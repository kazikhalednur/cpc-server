from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import OTP, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "gender",
                    "phone_number",
                    "picture",
                    "student_id",
                    "batch_no",
                    "batch_inital",
                    "department",
                    "email_verified",
                    "sub",
                    "is_complete",
                )
            },
        ),
        (
            "Social Links",
            {
                "fields": (
                    "facebook",
                    "twitter",
                    "instagram",
                    "linkedin",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password1", "password2"),
            },
        ),
    )

    list_display = ("email", "first_name", "last_name", "is_staff")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("first_name", "last_name", "email")
    ordering = ("id",)


admin.site.register(OTP)
