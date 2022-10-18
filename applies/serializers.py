from rest_framework import serializers
from .models import Apply
from recruits.serializers import RecruitListSerializer
from users.serializers import UserSerializer


class ApplySerializer(serializers.ModelSerializer):
    recruit = RecruitListSerializer(read_only=True)
    user = UserSerializer(read_only=True)

    class Meta:
        model = Apply
        fields = "__all__"
