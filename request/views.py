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
    

    @action(detail=False, methods=['get'], url_path='par-banque/(?P<banque_id>[^/.]+)')
    def get_requetes_par_banque(self, request, banque_id=None):
        requetes = Requete.objects.filter(docteur__BanqueDeSang__id=banque_id).order_by('-date_requete')
        serializer = self.get_serializer(requetes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)