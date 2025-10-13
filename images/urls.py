from django.urls import path

from .views import ImageUploadView, TinyMCEImageUploadView

urlpatterns = [
    path("upload/", ImageUploadView.as_view(), name="image-upload"),
    path(
        "tinymce/upload/", TinyMCEImageUploadView.as_view(), name="tinymce-image-upload"
    ),
]
