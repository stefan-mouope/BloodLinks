from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Requete
from .serializers import RequeteSerializer
from notification.utils import send_notification_to_banque
from users.models import Docteur


class RequeteViewSet(viewsets.ModelViewSet):
    serializer_class = RequeteSerializer

    def get_queryset(self):
        """
        🔹 Filtrer les requêtes du docteur connecté.
        """
        try:
            docteur = Docteur.objects.get(user=self.request.user)
            return Requete.objects.filter(docteur=docteur).order_by('-date_requete')
        except Docteur.DoesNotExist:
            return Requete.objects.none()

    def perform_create(self, serializer):
        """
        🔹 Lorsqu'une requête est créée :
          - On associe automatiquement le docteur connecté
          - On envoie une notification à la banque liée à ce docteur
        """
        try:
            docteur = Docteur.objects.get(user=self.request.user)
        except Docteur.DoesNotExist:
            raise ValueError("Aucun docteur associé à cet utilisateur.")

        # Création de la requête avec le docteur associé
        requete = serializer.save(docteur=docteur)

        # Vérifier si le docteur est rattaché à une banque
        if docteur.BanqueDeSang:
            banque = docteur.BanqueDeSang

            # Envoi de la notification à la banque
            send_notification_to_banque(
                banque.id,
                title="Nouvelle requête reçue 🩸",
                body=(
                    f"Le docteur {docteur.nom} {docteur.prenom} "
                    f"a soumis une requête pour {requete.quantite} unités du groupe {requete.groupe_sanguin}."
                ),
                data={
                    "requete_id": str(requete.id),
                    "docteur": f"{docteur.nom} {docteur.prenom}",
                    "groupe": requete.groupe_sanguin
                }
            )
            print(f"✅ Notification envoyée à la banque {getattr(banque, 'nom', banque.id)}")
        else:
            print("⚠️ Ce docteur n'est associé à aucune banque — notification non envoyée.")

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
        🔹 Retourne toutes les requêtes pour une banque spécifique.
        """
        requetes = Requete.objects.filter(
            docteur__BanqueDeSang__id=banque_id,
            statut='en_attente'
        ).order_by('-date_requete')
        serializer = self.get_serializer(requetes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
