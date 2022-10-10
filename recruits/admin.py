from django.contrib import admin
from .models import Recruit


@admin.register(Recruit)
class RecruitAdmin(admin.ModelAdmin):

    list_display = (
        "company",
        "position",
        "reward",
        "description",
        "skill",
    )
    list_filter = (
        "position",
        "skill",
        "company",
    )
