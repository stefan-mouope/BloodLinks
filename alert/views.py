from rest_framework import viewsets, status
from rest_framework.response import  Response
from rest_framework.views import APIView
from .models import Alerte, RecevoirAlerte

from .serializers import AlerteSerializer, AlerteSimpleSerializer, RecevoirAlerteSerializer

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
                statut="envoyee",
                requete__docteur__BanqueDeSang_id=banque_id
            )
            .select_related(
                "requete",
                "requete__docteur",
                "requete__docteur__BanqueDeSang"
            )
            .order_by("-date_envoi")
        )

        if not alertes.exists():
            return Response(
                {"detail": f"Aucune alerte envoyée pour la banque {banque_id}."},
                status=status.HTTP_404_NOT_FOUND
            )

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




class RecevoirAlerteViewSet(viewsets.ModelViewSet):
    queryset = RecevoirAlerte.objects.all().order_by('-date_reception')
    serializer_class = RecevoirAlerteSerializer

    def partial_update(self, request, *args, **kwargs):
        instance = self.get_object()
        nouveau_statut = request.data.get('statut')

        # Vérifie le statut de l'alerte principale
        if instance.alerte.statut != 'envoyee':
            return Response(
                {"detail": f"Cette alerte a déjà été traitée ({instance.alerte.statut})."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Cas où le donneur accepte l’alerte
        if nouveau_statut == 'accepte':
            instance.statut = 'accepte'
            instance.save()

            # On met aussi à jour l'alerte principale
            instance.alerte.statut = 'acceptee'
            instance.alerte.save()

            # Tous les autres receveurs pour la même alerte sont refusés
            RecevoirAlerte.objects.filter(
                alerte=instance.alerte
            ).exclude(id=instance.id).update(statut='refuse')

        else:
            # Simple mise à jour du statut (refus, etc.)
            instance.statut = nouveau_statut
            instance.save()

        serializer = self.get_serializer(instance)
        return Response(serializer.data)
