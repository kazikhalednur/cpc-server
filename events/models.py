from uuid import uuid4

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from committees.models import Wing


class EventSpeaker(models.Model):
    name = models.CharField(max_length=255)
    designation = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, default="Bangladesh")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class EventGuest(models.Model):
    name = models.CharField(max_length=255)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    organization = models.CharField(max_length=255, blank=True, null=True)
    country = models.CharField(max_length=255, default="Bangladesh")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    def __str__(self):
        return self.name


class EventManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(status="PUBLISHED", **kwargs)

    def archived(self, **kwargs):
        return self.filter(status="ARCHIVED", **kwargs)

    def draft(self, **kwargs):
        return self.filter(status="DRAFT", **kwargs)


class Event(models.Model):
    class EventStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    id = models.UUIDField(blank=True, primary_key=True, serialize=False, editable=False)
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    short_description = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to="events/")
    speakers = models.ManyToManyField(EventSpeaker, blank=True)
    guests = models.ManyToManyField(EventGuest, blank=True)
    event_date = models.DateTimeField()
    registration_deadline = models.DateTimeField(blank=True, null=True)
    registration_link = models.URLField(blank=True, null=True)
    venue = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20, choices=EventStatus.choices, default=EventStatus.DRAFT
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    objects = EventManager()

    class Meta:
        ordering = ["-event_date"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        if self.status == self.EventStatus.PUBLISHED and not self.published_at:
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
        return timezone.now() < self.event_date

    @property
    def is_ongoing(self):
        """Check if event is ongoing"""
        return (
            timezone.now() >= self.event_date
            and timezone.now() <= self.registration_deadline
        )

    @property
    def is_completed(self):
        """Check if event is completed"""
        return timezone.now() > self.registration_deadline

    @property
    def get_status_display(self):
        """Get the status display"""
        if self.is_upcoming:
            return "UPCOMING"
        elif self.is_ongoing:
            return "ONGOING"
        elif self.is_completed:
            return "COMPLETED"
