from django.db import models


class Profile(models.Model):
    class Wings(models.TextChoices):
        ACM = "ACM", "ACM"
        DEV = "DEV", "DEV"
        RJ = "RJ", "RJ"
        JCIC = "JCIC", "JCIC"

    bio = models.TextField(blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    location = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        abstract = True
