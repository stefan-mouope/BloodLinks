from django.urls import path, include
from rest_framework import routers
from .views import FaireDonViewSet, DonViewSet

router = routers.DefaultRouter()
router.register(r'fairedons', FaireDonViewSet)
router.register(r'dons', DonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
