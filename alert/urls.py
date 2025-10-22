from django.urls import path, include
from rest_framework import routers
from .views import AlerteViewSet

router = routers.DefaultRouter()
router.register(r'alertes', AlerteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
