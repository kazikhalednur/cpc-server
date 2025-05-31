from django.db import models


class Wing(models.Model):
    title = models.CharField(max_length=50)
    short_title = models.CharField(max_length=10, unique=True)
    position_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["position_order"]

    def __str__(self):
        return f"{self.title} ({self.short_title})"
