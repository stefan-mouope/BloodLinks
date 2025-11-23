from rest_framework import viewsets, status
from rest_framework.response import  Response
from rest_framework.views import APIView
from .models import Alerte, RecevoirAlerte
from rest_framework.decorators import action
from .serializers import AlerteSerializer, AlerteSimpleSerializer, RecevoirAlerteSerializer
from notifications.utils import send_notification_to_banque


class AlertesEnvoyeesParBanqueView(APIView):
    """
    🔹 Retourne toutes les alertes envoyées pour une banque spécifique.
    Exemple : /api/alertes/banque/?banque_id=1
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        banque_id = request.query_params.get("banque_id")
        if not banque_id:
            return Response(
                {"detail": "Le paramètre 'banque_id' est requis dans l'URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtrer les alertes envoyées pour cette banque
        alertes = (
            Alerte.objects
            .filter(
                statut="en_attente",
                requete__docteur__BanqueDeSang_id=banque_id
            )
            .select_related(
                "requete",
                "requete__docteur",
                "requete__docteur__BanqueDeSang"
            )
            .order_by("-date_envoi")
        )

        # if not alertes.exists():
        #     return Response(
        #         {"detail": f"Aucune alerte envoyée pour la banque {banque_id}."},
        #         status=status.HTTP_404_NOT_FOUND
        #     )

        serializer = AlerteSimpleSerializer(alertes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class AlerteParGroupeView(APIView):
    """
    🔹 Retourne toutes les alertes envoyées pour un groupe sanguin donné.
    Exemple : /api/alertes/groupe/?groupe_sanguin=O+
    """
    # permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # 🩸 Récupérer le paramètre dans l'URL
        groupe_sanguin = request.query_params.get("groupe_sanguin")

        if not groupe_sanguin:
            return Response(
                {"detail": "Le paramètre 'groupe_sanguin' est requis dans l'URL."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 🧩 Filtrer les alertes envoyées pour ce groupe sanguin
        alertes = (
            Alerte.objects
            .filter(
                statut="envoyee",
                requete__groupe_sanguin=groupe_sanguin
            )
            .select_related("requete__docteur", "requete__docteur__BanqueDeSang")
            .order_by("-date_envoi")
        )

        

        if not alertes.exists():
            return Response(
                {"detail": f"Aucune alerte trouvée pour le groupe sanguin {groupe_sanguin}."},
                status=status.HTTP_404_NOT_FOUND
            )

        serializer = AlerteSimpleSerializer(alertes, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class AlerteViewSet(viewsets.ModelViewSet):
    queryset = Alerte.objects.all().order_by('-date_envoi')
    serializer_class = AlerteSerializer

    @action(detail=True, methods=['patch'], url_path='mettre-a-jour-statut')
    def mettre_a_jour_statut(self, request, pk=None):
        """
        🔹 Met à jour le statut d'une alerte.
        Le nouveau statut doit être fourni dans le corps de la requête :
        {
            "statut": "en_attente", "envoyee","acceptee" / "refuse" / ...
        }
        """
        alert = self.get_object()
        nouveau_statut = request.data.get('statut')

        if not nouveau_statut:
            return Response(
                {"detail": "Le champ 'statut' est requis."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if alert.statut == nouveau_statut:
            return Response(
                {"detail": f"L'alerte a déjà le statut '{nouveau_statut}'."},
                status=status.HTTP_400_BAD_REQUEST
            )

     
        alert.statut = nouveau_statut
        alert.save()

        if nouveau_statut == "acceptee":
            if hasattr(alert, 'requete') and alert.requete:
                alert.requete.statut = 'valide' 
                alert.requete.save()

        serializer = self.get_serializer(alert)
        return Response(serializer.data, status=status.HTTP_200_OK)



class RecevoirAlerteViewSet(viewsets.ModelViewSet):
    queryset = RecevoirAlerte.objects.all().order_by('-date_reception')
    serializer_class = RecevoirAlerteSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        nouveau_statut = request.data.get('statut')
        print('teste', instance.alerte.id)
        
        # Vérifie le statut de l'alerte principale
        if instance.alerte.statut != 'en_attente' :
            return Response(
                {"detail": f"Cette alerte a déjà été traitée ({instance.alerte.statut})."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cas où le donneur accepte l’alerte
        if nouveau_statut == 'en_attente':
            print(nouveau_statut)
            instance.alerte.statut = 'en_attente'
            instance.alerte.save()

            # Refuser les autres receveurs
            RecevoirAlerte.objects.filter(
                alerte=instance.alerte
            ).exclude(id=instance.id).update(statut='refuse')

            # ✅ Notification à la Banque de Sang
            requete = instance.alerte.requete
            if requete and requete.docteur and requete.docteur.BanqueDeSang:
                banque_id = requete.docteur.BanqueDeSang.id
                send_notification_to_banque(
                    banque_id,
                    title="Nouvelle alerte en attente ⚠️",
                    body=f"Une alerte pour le groupe {requete.groupe_sanguin} est en attente.",
                    data={"alerte_id": str(instance.alerte.id)}
                )

        else:
            # Simple mise à jour du statut de la réception
            instance.statut = nouveau_statut
            instance.save()

        # 🔹 Sérialiser l’alerte liée plutôt que la réception
        from .serializers import AlerteSerializer
        alerte_serializer = AlerteSerializer(instance.alerte)

        return Response(alerte_serializer.data, status=status.HTTP_200_OK)