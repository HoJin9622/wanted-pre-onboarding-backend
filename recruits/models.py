from django.db import models
from common.models import CommonModel


class Recruit(CommonModel):

    """Recruit Model Definition"""

    position = models.CharField(
        max_length=40,
        verbose_name="채용포지션",
    )
    reward = models.PositiveIntegerField(
        verbose_name="채용보상금",
    )
    description = models.TextField(
        verbose_name="채용내용",
    )
    skill = models.CharField(
        max_length=40,
        verbose_name="사용기술",
    )
    company = models.ForeignKey(
        "companies.Company",
        on_delete=models.CASCADE,
        related_name="recruits",
        verbose_name="채용회사",
    )
