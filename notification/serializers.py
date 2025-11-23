from rest_framework import serializers
from .models import FCMToken

# class notificationerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Notification
#         fields = ['id', 'user', 'title', 'body', 'created_at', 'updated_at']

class FCMTokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = FCMToken
        fields = ['id', 'user', 'token', 'device_name', 'created_at', 'updated_at']