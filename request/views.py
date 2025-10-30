from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Requete
from .serializers import RequeteSerializer

class RequeteViewSet(viewsets.ModelViewSet):
    queryset = Requete.objects.all().order_by('-date_requete')
    serializer_class = RequeteSerializer

    @action(detail=True, methods=['patch'], url_path='mettre-a-jour-statut')
    def mettre_a_jour_statut(self, request, pk=None):
        """
        🔹 Met à jour le statut d'une requête.
        Le nouveau statut doit être fourni dans le corps de la requête:
        {
            "statut": "valide" / "refuse" / ...
        }
        """
        requete = self.get_object()
        nouveau_statut = request.data.get('statut')

        if not nouveau_statut:
            return Response(
                {"detail": "Le champ 'statut' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if requete.statut == nouveau_statut:
            return Response(
                {"detail": f"La requête a déjà le statut '{nouveau_statut}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Mettre à jour le statut
        requete.statut = nouveau_statut
        requete.save()
        serializer = self.get_serializer(requete)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @action(detail=False, methods=['get'], url_path='par-banque/(?P<banque_id>[^/.]+)')
    def get_requetes_par_banque(self, request, banque_id=None):
        """
        🔹 Retourne toutes les requêtes pour une banque spécifique
        """
        requetes = Requete.objects.filter(docteur__BanqueDeSang__id=banque_id).order_by('-date_requete')
        serializer = self.get_serializer(requetes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
