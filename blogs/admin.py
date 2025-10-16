from django.contrib import admin

from .models import Blog, BlogBookmark, BlogCategory, BlogLike

admin.site.register(BlogCategory)
admin.site.register(Blog)
admin.site.register(BlogLike)
admin.site.register(BlogBookmark)
