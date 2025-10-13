from django.contrib import admin

from .models import Image, TinyMCEImage

admin.site.register(Image)
admin.site.register(TinyMCEImage)
