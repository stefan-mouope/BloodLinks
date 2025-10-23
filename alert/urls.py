from django.urls import path, include
from rest_framework import routers
from .views import AlerteViewSet, RecevoirAlerteViewSet

router = routers.DefaultRouter()
router.register(r'alertes', AlerteViewSet)
router.register(r'recevoir_alerte', RecevoirAlerteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
