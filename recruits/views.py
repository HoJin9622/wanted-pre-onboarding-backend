from django.db.models import Q
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import ParseError, NotFound
from companies.models import Company
from .models import Recruit
from .serializers import RecruitListSerializer, RecruitDetailSerializer


class Recruits(APIView):
    def get(self, request):
        recruits = Recruit.objects.all()
        search = self.request.query_params.get("search")

        if search is not None:
            recruits = recruits.filter(
                Q(position__icontains=search)
                | Q(skill__icontains=search)
                | Q(company__name__icontains=search)
            )

        serializer = RecruitListSerializer(recruits, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = RecruitDetailSerializer(data=request.data)
        company_id = request.data.get("company_id")

        if not company_id:
            raise ParseError("Company id is required.")

        if serializer.is_valid():
            try:
                company = Company.objects.get(id=company_id)
            except Company.DoesNotExist:
                raise ParseError("Company not found.")
            recruit = serializer.save(company=company)
            serializer = RecruitDetailSerializer(recruit)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)


class RecruitDetail(APIView):
    def get_object(self, pk):
        try:
            return Recruit.objects.get(pk=pk)
        except Recruit.DoesNotExist:
            raise NotFound

    def get(self, request, pk):
        recruit = self.get_object(pk)
        serializer = RecruitDetailSerializer(recruit)
        return Response(serializer.data)

    def put(self, request, pk):
        recruit = self.get_object(pk)
        serializer = RecruitDetailSerializer(
            recruit,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            recruit = serializer.save()
            serializer = RecruitDetailSerializer(recruit)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        recruit = self.get_object(pk)
        recruit.delete()
        return Response(HTTP_204_NO_CONTENT)


# class RecruitViewSet(ModelViewSet):
#     queryset = Recruit.objects.all()

#     def get_serializer_class(self):
#         if self.action == "retrieve":
#             return RecruitDetailSerializer
#         return RecruitListSerializer

#     def get_queryset(self):
#         queryset = Recruit.objects.all()
#         search = self.request.query_params.get("search")
#         if search is not None:
#             queryset = queryset.filter(
#                 Q(position__icontains=search)
#                 | Q(skill__icontains=search)
#                 | Q(company__name__icontains=search)
#             )
#         return queryset
