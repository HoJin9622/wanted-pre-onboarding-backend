from rest_framework.routers import DefaultRouter
from . import views

app_name = "recruits"


router = DefaultRouter()
router.register("", views.RecruitViewSet)
urlpatterns = router.urls
