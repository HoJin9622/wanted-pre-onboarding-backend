from django.db import models
from common.models import CommonModel


class Company(CommonModel):

    """Company Model Definition"""

    class CompanyNationChoices(models.TextChoices):
        KOREA = ("korea", "한국")
        JAPAN = ("japan", "일본")
        CHINA = ("china", "중국")

    name = models.CharField(
        max_length=80,
        verbose_name="회사명",
    )
    nation = models.CharField(
        max_length=28,
        choices=CompanyNationChoices.choices,
        verbose_name="국가",
    )
    area = models.CharField(
        max_length=60,
        verbose_name="지역",
    )

    class Meta:
        verbose_name_plural = "Companies"

    def __str__(self):
        return self.name
