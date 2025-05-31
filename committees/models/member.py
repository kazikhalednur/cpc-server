from django.db import models
from django.utils import timezone

from accounts.models import User

from .core_position import CorePosition
from .wing import Wing


class Member(models.Model):
    class MemberType(models.TextChoices):
        GENERAL = "GENERAL", "General"
        ASSOCIATE = "ASSOCIATIVE", "Associative"
        EXECUTIVE = "EXECUTIVE", "Executive"
        CORE = "CORE", "Core"

    def get_year_choices(start_year=2000):
        current_year = timezone.now().year
        return [(year, str(year)) for year in range(start_year, current_year + 1)]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    year = models.IntegerField(choices=get_year_choices(), default=timezone.now().year)
    member_type = models.CharField(max_length=20, choices=MemberType.choices)
    wing = models.ForeignKey(Wing, on_delete=models.CASCADE)
    position = models.ForeignKey(CorePosition, on_delete=models.CASCADE)
    joined_at = models.DateTimeField()
    ended_at = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.get_full_name()} {self.member_type} - {self.wing} - {self.position}"  # noqa: E501
