from django.db import models


class CorePosition(models.Model):
    title = models.CharField(max_length=50)
    position_order = models.PositiveIntegerField(
        default=0,
        blank=False,
        null=False,
    )

    class Meta:
        ordering = ["position_order"]
        verbose_name = "Core Committee Position"
        verbose_name_plural = "Core Committee Positions"

    def __str__(self):
        return self.title
