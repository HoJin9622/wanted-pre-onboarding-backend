from django.db import models
from common.models import CommonModel


class Apply(CommonModel):

    recruit = models.ForeignKey(
        "recruits.Recruit",
        on_delete=models.CASCADE,
        related_name="applies",
        verbose_name="채용공고",
    )
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="applies",
        verbose_name="지원자",
    )
