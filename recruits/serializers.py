from rest_framework import serializers
from companies.models import Company
from .models import Recruit


class RecruitSerializer(serializers.ModelSerializer):
    company_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Recruit
        exclude = ()
        read_only_fields = ("company",)

    def validate_company_id(self, value):
        request = self.context.get("request")
        if request.method == "PATCH":
            raise serializers.ValidationError("company_id can not be modified")
        try:
            Company.objects.get(pk=value)
            return value
        except Company.DoesNotExist:
            raise serializers.ValidationError("Not exists company")

    def create(self, validated_data):
        recruit = Recruit.objects.create(**validated_data)
        return recruit
