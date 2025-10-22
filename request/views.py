from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Requete
from .serializers import RequeteSerializer

class RequeteViewSet(viewsets.ModelViewSet):
    queryset = Requete.objects.all().order_by('-date_requete')
    serializer_class = RequeteSerializer

    @action(detail=True, methods=['patch'], url_path='valider')
    def valider_requete(self, request, pk=None):
        requete = self.get_object()
        if requete.statut == 'valide':
            return Response({"detail": "Cette requête est déjà validée."},
                            status=status.HTTP_400_BAD_REQUEST)
        
        # Valider la requête
        requete.statut = 'valide'
        requete.save()
        serializer = self.get_serializer(requete)
        return Response(serializer.data)