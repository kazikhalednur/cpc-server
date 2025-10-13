from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from drf_spectacular.utils import extend_schema, inline_serializer
from rest_framework import serializers, status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from .models import TinyMCEImage
from .serializers import ImageSerializer


class ImageUploadView(CreateAPIView):
    serializer_class = ImageSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @extend_schema(
        responses={
            201: inline_serializer(
                name="ImageUploadViewResponse",
                fields={
                    "message": serializers.CharField(
                        default="Image uploaded successfully"
                    ),
                },
            ),
        },
    )
    def create(self, request, *args, **kwargs):
        super().create(request, *args, **kwargs)
        return Response(
            {"message": "Image uploaded successfully"}, status=status.HTTP_201_CREATED
        )


@method_decorator(csrf_exempt, name="dispatch")  # TinyMCE may not send CSRF
class TinyMCEImageUploadView(View):
    """Authenticated image upload endpoint for TinyMCE."""

    @method_decorator(login_required)
    def post(self, request, *args, **kwargs):
        if "file" not in request.FILES:
            return JsonResponse({"error": "No file uploaded"}, status=400)

        file = request.FILES["file"]

        if not file.content_type.startswith("image/"):
            return JsonResponse({"error": "Only image uploads allowed"}, status=400)

        if file.size > 5 * 1024 * 1024:  # 5 MB
            return JsonResponse({"error": "File too large (max 5 MB)"}, status=400)

        uploaded_image: TinyMCEImage = TinyMCEImage.objects.create(
            user=request.user, file=file
        )
        file_url = request.build_absolute_uri(uploaded_image.file.url)

        return JsonResponse({"location": file_url})
