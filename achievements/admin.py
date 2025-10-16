from django.contrib import admin
from simple_history.admin import SimpleHistoryAdmin

from .models import Achievement


@admin.register(Achievement)
class AchievementAdmin(SimpleHistoryAdmin):
    list_display = (
        "title",
        "team_name",
        "rank",
        "date",
        "status",
        "created_at",
    )
    list_filter = ("status", "date", "created_at")
    search_fields = ("title", "team_name", "rank")
    ordering = ("-date", "-created_at")
    readonly_fields = ("created_at", "updated_at")

    fieldsets = (
        (
            None,
            {
                "fields": ("title", "team_name", "rank", "status", "date"),
            },
        ),
        (
            "Media & Content",
            {
                "fields": ("image", "description"),
            },
        ),
        (
            "Timestamps",
            {
                "fields": ("created_at", "updated_at"),
            },
        ),
    )
