from django.contrib import admin

from .models import Notice, NoticeCategory, NoticeTag

admin.site.register(NoticeCategory)
admin.site.register(NoticeTag)


@admin.register(Notice)
class NoticeAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "priority",
        "status",
        "is_pinned",
        "published_at",
        "created_at",
    ]
    list_filter = [
        "status",
        "priority",
        "is_pinned",
        "category",
        "tags",
        "created_at",
        "published_at",
    ]
    search_fields = ["title", "content"]
    filter_horizontal = ["tags"]
    readonly_fields = ["id", "created_at", "updated_at"]

    fieldsets = (
        ("Basic Information", {"fields": ("title", "content", "category", "tags")}),
        ("Settings", {"fields": ("priority", "status", "is_pinned")}),
        (
            "Timestamps",
            {
                "fields": ("published_at", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )

    def save_model(self, request, obj, form, change):
        # Auto-set published_at when status changes to PUBLISHED
        if obj.status == "PUBLISHED" and not obj.published_at:
            from django.utils import timezone

            obj.published_at = timezone.now()
        super().save_model(request, obj, form, change)
