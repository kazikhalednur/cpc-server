from django.db import models


class PersonalInfo(models.Model):
    class Gender(models.TextChoices):
        MALE = "MALE", "Male"
        FEMALE = "FEMALE", "Female"
        OTHER = "OTHER", "Other"

    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150, blank=True, null=True)
    picture = models.URLField(max_length=300, blank=True, null=True)
    student_id = models.CharField(max_length=20, unique=True)
    batch_no = models.CharField(max_length=10, blank=True, null=True)
    batch_inital = models.CharField(max_length=10, blank=True, null=True)
    department = models.CharField(max_length=100, blank=True, null=True)

    gender = models.CharField(
        max_length=10, choices=Gender.choices, blank=True, null=True
    )
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)

    class Meta:
        abstract = True
