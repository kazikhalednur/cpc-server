from uuid import uuid4

from django.db import models


class Committee(models.Model):
    id = models.UUIDField(blank=True, primary_key=True, serialize=False, editable=False)
    year = models.CharField(max_length=4)

    class Meta:
        ordering = ["-year"]
        verbose_name = "Committee"
        verbose_name_plural = "Committees"

    def __str__(self):
        return f"The {self.year} Committee"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super().save(*args, **kwargs)
