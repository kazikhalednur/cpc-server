from django.db.models.signals import post_delete, pre_save
from django.dispatch import receiver

from .models import Blog
from .utils import generate_unique_slug


@receiver(pre_save, sender=Blog)
def generate_slug(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = generate_unique_slug(Blog, instance.title, "slug")


@receiver(post_delete, sender=Blog)
def delete_image(sender, instance, *args, **kwargs):
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_save, sender=Blog)
def update_slug_when_title_changes(sender, instance, *args, **kwargs):
    try:
        if instance.id:
            if instance.title != instance.__class__.objects.get(id=instance.id).title:
                instance.slug = generate_unique_slug(Blog, instance.title, "slug")
    except Blog.DoesNotExist:
        pass
