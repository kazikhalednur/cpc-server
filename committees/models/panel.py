from uuid import uuid4

from django.db import models

from .committee import Committee


class Panel(models.Model):
    class PanelType(models.TextChoices):
        ADVISOR = "ADVISOR", "Advisor"
        STUDENT = "STUDENT", "Student"

    id = models.UUIDField(blank=True, primary_key=True, serialize=False, editable=False)
    committee: Committee = models.ForeignKey(
        Committee, on_delete=models.CASCADE, related_name="panels"
    )
    type = models.CharField(max_length=20, choices=PanelType.choices)
    image = models.ImageField(upload_to="panels/")

    def __str__(self):
        return f"{self.type} Panel {self.committee.year}"

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super().save(*args, **kwargs)
