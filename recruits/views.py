from django.db.models import Q
from rest_framework.viewsets import ModelViewSet
from .models import Recruit
from .serializers import RecruitListSerializer, RecruitDetailSerializer


class RecruitViewSet(ModelViewSet):
    queryset = Recruit.objects.all()

    def get_serializer_class(self):
        if self.action == "retrieve":
            return RecruitDetailSerializer
        return RecruitListSerializer

    def get_queryset(self):
        queryset = Recruit.objects.all()
        search = self.request.query_params.get("search")
        if search is not None:
            queryset = queryset.filter(
                Q(position__icontains=search)
                | Q(skill__icontains=search)
                | Q(company__name__icontains=search)
            )
        return queryset
