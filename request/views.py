from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Requete
from .serializers import RequeteSerializer
from notifications.utils import send_notification_to_banque  # ⚠️ fonction vue précédemment

class RequeteViewSet(viewsets.ModelViewSet):
    queryset = Requete.objects.all().order_by('-date_requete')
    serializer_class = RequeteSerializer

    def perform_create(self, serializer):
        """
        🔹 Appelée automatiquement à la création d'une requête.
        On envoie une notification à la banque du docteur.
        """
        requete = serializer.save()  # On crée la requête normalement

        # Vérifier si la requête a bien un docteur et une banque
        if requete.docteur and requete.docteur.BanqueDeSang:
            banque = requete.docteur.BanqueDeSang

            # Envoi de la notification à la banque
            send_notification_to_banque(
                banque.id,
                title="Nouvelle requête reçue 🩸",
                body=f"Le docteur {requete.docteur.nom} {requete.docteur.prenom} "
                     f"a soumis une requête pour {requete.quantite} unités du groupe {requete.groupe_sanguin}.",
                data={
                    "requete_id": str(requete.id),
                    "docteur": f"{requete.docteur.nom} {requete.docteur.prenom}",
                    "groupe": requete.groupe_sanguin
                }
            )
            print(f"✅ Notification envoyée à la banque {banque.nom if hasattr(banque, 'nom') else banque.id}")

        else:
            print("⚠️ Aucun docteur ou banque associée à cette requête — aucune notification envoyée.")

    @action(detail=True, methods=['patch'], url_path='mettre-a-jour-statut')
    def mettre_a_jour_statut(self, request, pk=None):
        """
        🔹 Met à jour le statut d'une requête.
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
