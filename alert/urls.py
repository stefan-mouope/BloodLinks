from django.urls import path, include
from rest_framework import routers
from .views import AlerteViewSet, RecevoirAlerteViewSet,AlerteParGroupeView,AlertesEnvoyeesParBanqueView

router = routers.DefaultRouter()
router.register(r'', AlerteViewSet)
router.register(r'recevoir_alerte', RecevoirAlerteViewSet)

urlpatterns = [
    path('banque/', AlertesEnvoyeesParBanqueView.as_view(), name='alertes-envoyees-banque'),
    path('par-groupe/', AlerteParGroupeView.as_view(), name='alertes-par-groupe'),
    path('', include(router.urls)),
   
]
