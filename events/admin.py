from django.contrib import admin

from .models import Event, EventGuest, EventSpeaker

admin.site.register(EventSpeaker)
admin.site.register(EventGuest)
admin.site.register(Event)
