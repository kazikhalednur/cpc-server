from adminsortable2.admin import SortableAdminMixin
from django.contrib import admin

from .models import Committee, CorePosition, Member, Panel, Wing


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    list_display = ["year"]
    search_fields = ["year"]
    list_filter = ["year"]


@admin.register(Panel)
class PanelAdmin(admin.ModelAdmin):
    list_display = ["committee", "type", "image"]


admin.site.register(Member)


@admin.register(Wing)
class SortableWingAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["title", "short_title"]


@admin.register(CorePosition)
class SortableCorePositionAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ["title"]
