from rest_framework.viewsets import ModelViewSet
from .models import Recruit
from .serializers import RecruitSerializer


class RecruitViewSet(ModelViewSet):

    queryset = Recruit.objects.all()
    serializer_class = RecruitSerializer
