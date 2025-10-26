# notifications/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_push_notification
from .models import FCMToken, Notification
from .serializers import FCMTokenSerializer, NotificationSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets

class FCMTokenViewSet(viewsets.ModelViewSet):
    queryset = FCMToken.objects.all()
    serializer_class = FCMTokenSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



@api_view(['POST'])
def send_notification(request):
    """
    Envoie une notification à un appareil (token reçu depuis le frontend)
    """
    token = request.data.get("token")
    title = request.data.get("title", "Notification")
    body = request.data.get("body", "Ceci est un message de test")
    
    if not token:
        return Response({"error": "Le token est requis"}, status=400)
    
    success = send_push_notification(token, title, body)
    return Response({"success": success})


