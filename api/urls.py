
from django.urls import path, include
from rest_framework import routers
from api.views import getLocationsWithinDistance, UserModelViewSet


router = routers.DefaultRouter()

router.register(
    r"users",
    UserModelViewSet,
    basename="user",
)

router.register(
    r"locations",
    getLocationsWithinDistance,
    basename="location",
)



urlpatterns = [
    path("", include(router.urls)),
]