# notifications/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .utils import send_push_notification
from .models import FCMToken
from .serializers import FCMTokenSerializer
from rest_framework import status
from rest_framework.views import APIView
from rest_framework import viewsets

class FCMTokenViewSet(viewsets.ModelViewSet):
    queryset = FCMToken.objects.all()
    serializer_class = FCMTokenSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        # l'utilisateur ne voit que ses propres tokens
        return FCMToken.objects.filter(user=self.request.user)


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


from django.db import connection
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status

@api_view(['DELETE'])
# @permission_classes([IsAdminUser])  # 🔒 Seulement les admins peuvent l’exécuter
def reset_database(request):
    """
    Supprime toutes les tables du schéma 'public' dans la base PostgreSQL.
    ⚠️ Attention : cette opération est irréversible.
    """
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                DO $$ DECLARE
                    r RECORD;
                BEGIN
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'public') LOOP
                        EXECUTE 'TRUNCATE TABLE public.' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
                    END LOOP;
                END $$;
            """)
        return Response({"message": "Toutes les tables ont été vidées avec succès."}, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)