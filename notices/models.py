from uuid import uuid4

from django.db import models
from django.utils.text import slugify
from simple_history.models import HistoricalRecords


class NoticeCategory(models.Model):
    title = models.CharField(max_length=200, unique=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Notice Category"
        verbose_name_plural = "Notice Categories"

    def __str__(self):
        return self.title


class NoticeTag(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)


class NoticeManager(models.Manager):
    def published(self, **kwargs):
        return self.filter(status="PUBLISHED", **kwargs)

    def draft(self, **kwargs):
        return self.filter(status="DRAFT", **kwargs)

    def archived(self, **kwargs):
        return self.filter(status="ARCHIVED", **kwargs)


class Notice(models.Model):
    class Priority(models.TextChoices):
        HIGH = "HIGH", "High"
        MEDIUM = "MEDIUM", "Medium"
        LOW = "LOW", "Low"

    class Status(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    id = models.UUIDField(blank=True, primary_key=True, serialize=False, editable=False)
    title = models.CharField(max_length=200)
    content = models.TextField()
    category = models.ForeignKey(NoticeCategory, on_delete=models.CASCADE)
    priority = models.CharField(max_length=20, choices=Priority.choices)
    tags = models.ManyToManyField(NoticeTag, blank=True)
    is_pinned = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=Status.choices)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(blank=True, null=True)

    history = HistoricalRecords()

    objects = NoticeManager()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        super().save(*args, **kwargs)
