from django.urls import path, include
from rest_framework import routers
from .views import AlerteViewSet, RecevoirAlerteViewSet,AlerteParGroupeView

router = routers.DefaultRouter()
router.register(r'alertes', AlerteViewSet)
router.register(r'recevoir_alerte', RecevoirAlerteViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('par-groupe/', AlerteParGroupeView.as_view(), name='alertes-par-groupe')
]
