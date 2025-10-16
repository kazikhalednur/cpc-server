import uuid

from django.db import models
from simple_history.models import HistoricalRecords
from tinymce.models import HTMLField


class AchievementManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(status="PUBLISHED", **kwargs)

    def draft(self, **kwargs):
        return self.filter(status="DRAFT", **kwargs)

    def archived(self, **kwargs):
        return self.filter(status="ARCHIVED", **kwargs)


class Achievement(models.Model):
    class AchievementStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255)
    team_name = models.CharField(max_length=255)
    rank = models.CharField(max_length=255)
    image = models.ImageField(upload_to="achievements/")
    description = HTMLField()
    date = models.DateField()
    status = models.CharField(max_length=255, choices=AchievementStatus.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()
    objects = AchievementManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid.uuid4()
        super().save(*args, **kwargs)
