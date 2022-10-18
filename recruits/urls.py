from django.urls import path
from . import views

urlpatterns = [
    path("", views.Recruits.as_view()),
    path("<int:pk>", views.RecruitDetail.as_view()),
]
