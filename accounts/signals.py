from django.db.models.signals import pre_save
from django.dispatch import receiver
from rest_framework_simplejwt.token_blacklist.models import (
    BlacklistedToken,
    OutstandingToken,
)

from .models import User


@receiver(pre_save, sender=User)
def revoke_tokens(sender, instance, update_fields, **kwargs):
    if (
        not instance._state.adding
    ):  # instance._state.adding gives true if object is being created for the first time  # noqa: E501
        existing_user = User.objects.get(pk=instance.pk)
        if (
            instance.password != existing_user.password
            or instance.email != existing_user.email
        ):
            # If any of these params have changed, blacklist the tokens
            outstanding_tokens = OutstandingToken.objects.filter(user__pk=instance.pk)
            # Not checking for expiry date as cron is supposed to flush the expired tokens  # noqa: E501
            # using manage.py flushexpiredtokens. But if You are not using cron,
            # then you can add another filter that expiry_date__gt=datetime.datetime.now()  # noqa: E501

            for out_token in outstanding_tokens:
                if hasattr(out_token, "blacklistedtoken"):
                    # Token already blacklisted. Skip
                    continue

                BlacklistedToken.objects.create(token=out_token)


@receiver(pre_save, sender=User)
def delete_old_avatar(sender, instance, *args, **kwargs):
    try:
        old_img = instance.__class__.objects.get(id=instance.id).avatar.path
        try:
            new_img = instance.avatar.path
        except:  # noqa: E722
            new_img = None
        if new_img != old_img:
            import os

            if os.path.exists(old_img):
                os.remove(old_img)
    except:  # noqa: E722
        pass
