from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import CorePosition, Member, Wing

admin.site.register(Member)


@admin.register(Wing)
class SortableWingAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["title", "short_title"]


@admin.register(CorePosition)
class SortableCorePositionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["title"]
