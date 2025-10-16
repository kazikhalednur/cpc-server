from uuid import uuid4

from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords
from tinymce.models import HTMLField

from accounts.models import User


class BlogCategory(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Blog Category"
        verbose_name_plural = "Blog Categories"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            from .utils import generate_unique_slug

            self.slug = generate_unique_slug(BlogCategory, self.title, "slug")
        super().save(*args, **kwargs)


class BlogManager(models.Manager):
    def pending(self, **kwargs):
        return self.filter(status="PENDING", **kwargs)

    def in_review(self, **kwargs):
        return self.filter(status="IN_REVIEW", **kwargs)

    def published(self, **kwargs):
        return self.filter(status="PUBLISHED", **kwargs)

    def archived(self, **kwargs):
        return self.filter(status="ARCHIVED", **kwargs)


class Blog(models.Model):
    class BlogStatus(models.TextChoices):
        DRAFT = "DRAFT", "Draft"
        PENDING = "PENDING", "Pending"
        IN_REVIEW = "IN_REVIEW", "In Review"
        PUBLISHED = "PUBLISHED", "Published"
        ARCHIVED = "ARCHIVED", "Archived"

    id = models.UUIDField(blank=True, primary_key=True, serialize=False, editable=False)
    category: BlogCategory = models.ForeignKey(BlogCategory, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    short_description = models.CharField(max_length=500)
    content = HTMLField()
    author: User = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to="blogs/")
    tags = models.CharField(max_length=150, blank=True, null=True)
    read_time = models.CharField(
        max_length=50, blank=True, null=True, help_text="8 min read"
    )
    views_count = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=20, choices=BlogStatus.choices)
    published_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BlogManager()
    history = HistoricalRecords()

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = uuid4()
        if self.status == self.BlogStatus.PUBLISHED and not self.published_at:
            self.published_at = timezone.now()
        super().save(*args, **kwargs)


class BlogLike(models.Model):
    blog: Blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="likes")
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Blog Like"
        verbose_name_plural = "Blog Likes"

    def __str__(self):
        return f"{self.user.username} liked {self.blog.title}"


class BlogBookmark(models.Model):
    blog: Blog = models.ForeignKey(
        Blog, on_delete=models.CASCADE, related_name="bookmarks"
    )
    user: User = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    history = HistoricalRecords()

    class Meta:
        verbose_name = "Blog Bookmark"
        verbose_name_plural = "Blog Bookmarks"

    def __str__(self):
        return f"{self.user.username} saved {self.blog.title}"
