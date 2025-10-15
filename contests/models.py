from uuid import uuid4

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from tinymce.models import HTMLField


class ContestManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(status="PUBLISHED", **kwargs)

    def draft(self, **kwargs):
        return self.filter(status="DRAFT", **kwargs)

    def archived(self, **kwargs):
        return self.filter(status="ARCHIVED", **kwargs)


class Contest(models.Model):
    class DifficultyLevel(models.TextChoices):
        EASY = "EASY", "Easy"
        MEDIUM = "MEDIUM", "Medium"
        HARD = "HARD", "Hard"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    id = models.UUIDField(blank=True, primary_key=True, serialize=False, editable=False)
    title = models.CharField(max_length=200)
    short_description = models.CharField(max_length=500)
    description = HTMLField()
    image = models.ImageField(upload_to="contests/")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    difficulty_level = models.CharField(max_length=20, choices=DifficultyLevel.choices)
    platform = models.CharField(max_length=200)
    platform_link = models.URLField(blank=True, null=True)
    participants = models.CharField(
        max_length=200, blank=True, null=True, help_text="Number of participants"
    )
    max_participants = models.PositiveIntegerField(
        blank=True, null=True, help_text="Maximum number of participants"
    )
    registration_link = models.URLField(blank=True, null=True)
    registration_deadline = models.DateTimeField(blank=True, null=True)
    organizer = models.CharField(max_length=200, blank=True, null=True)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    objects = ContestManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        if self.status == self.Status.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)

    @property
    def is_registration_open(self):
        """Check if registration is still open"""
        if not self.registration_deadline:
            return False
        return timezone.now() <= self.registration_deadline

    @property
    def is_upcoming(self):
        """Check if event is upcoming"""
        return timezone.now() < self.start_time

    @property
    def is_ongoing(self):
        """Check if event is ongoing"""
        return timezone.now() >= self.start_time and timezone.now() <= self.end_time

    @property
    def is_completed(self):
        """Check if event is completed"""
        return timezone.now() > self.end_time

    @property
    def get_status_display(self):
        """Get the status display"""
        if self.is_upcoming:
            return "UPCOMING"
        elif self.is_ongoing:
            return "ONGOING"
        elif self.is_completed:
            return "COMPLETED"


class Prize(models.Model):
    contest = models.ForeignKey(Contest, on_delete=models.CASCADE)
    title = models.CharField(
        max_length=200, help_text="1st prize, 2nd prize, 3rd prize, etc."
    )
    amount = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super().save(*args, **kwargs)
