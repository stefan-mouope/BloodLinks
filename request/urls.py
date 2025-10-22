from django.urls import path, include
from rest_framework import routers
from .views import RequeteViewSet

router = routers.DefaultRouter()
router.register(r'requetes', RequeteViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
