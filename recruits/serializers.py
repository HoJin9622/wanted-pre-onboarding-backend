from rest_framework import serializers
from .models import Recruit


class RecruitDetailSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    company_nation = serializers.SerializerMethodField()
    company_area = serializers.SerializerMethodField()
    other_recruits = serializers.SerializerMethodField()

    class Meta:
        model = Recruit
        fields = ("id", "position", "reward", "description", "skill")

    def get_company_name(self, obj):
        return obj.company.name

    def get_company_nation(self, obj):
        return obj.company.nation

    def get_company_area(self, obj):
        return obj.company.area

    def get_other_recruits(self, obj):
        recruits = obj.company.recruits.exclude(pk=obj.pk)
        return RecruitListSerializer(recruits, many=True).data


class RecruitListSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()
    company_nation = serializers.SerializerMethodField()
    company_area = serializers.SerializerMethodField()

    class Meta:
        model = Recruit
        fields = ("id", "position", "reward", "skill")

    def get_company_name(self, obj):
        return obj.company.name

    def get_company_nation(self, obj):
        return obj.company.nation

    def get_company_area(self, obj):
        return obj.company.area
