from django.urls import path, include
from rest_framework import routers
from .views import  DonViewSet

router = routers.DefaultRouter()
router.register(r'dons', DonViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
