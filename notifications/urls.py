# notifications/urls.py
from django.urls import path, include
from .views import send_notification, FCMTokenViewSet
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'fcm-tokens', FCMTokenViewSet, basename='fcm-token')

urlpatterns = [
    path("send/", send_notification, name="send-notification"),
    path('', include(router.urls)),
]
