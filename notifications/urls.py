# notifications/urls.py
from django.urls import path, include
from .views import send_notification, FCMTokenViewSet
from rest_framework.routers import DefaultRouter
from .views import reset_database


router = DefaultRouter()
router.register(r'fcm-tokens', FCMTokenViewSet, basename='fcm-token')

urlpatterns = [
    path("send/", send_notification, name="send-notification"),
    path('', include(router.urls)),
    # path('reset-db/', reset_database, name='reset-database'),
]
