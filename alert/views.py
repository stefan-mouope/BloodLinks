from rest_framework import viewsets, status
from rest_framework.response import  Response
from .models import Alerte, RecevoirAlerte
from .serializers import AlerteSerializer, RecevoirAlerteSerializer

class AlerteViewSet(viewsets.ModelViewSet):
    queryset = Alerte.objects.all().order_by('-date_envoi')
    serializer_class = AlerteSerializer


class RecevoirAlerteViewSet(viewsets.ModelViewSet):
    queryset = RecevoirAlerte.objects.all().order_by('-date_reception')
    serializer_class = RecevoirAlerteSerializer
    


    def partial_update(self, request, *args, **kwargs):
            instance = self.get_object()
            nouveau_statut = request.data.get('statut')

            # On bloque si déjà traité
            if instance.statut != 'en_attente':
                return Response(
                    {"detail": f"Cette alerte a déjà été traitée ({instance.statut})."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            if nouveau_statut == 'accepte':
                # Accepte ce don
                instance.statut = 'accepte'
                instance.save()
                # Refuse tous les autres pour la même alerte
                RecevoirAlerte.objects.filter(
                    alerte=instance.alerte
                ).exclude(id=instance.id).update(statut='refuse')
            else:
                instance.statut = nouveau_statut
                instance.save()

            serializer = self.get_serializer(instance)
            return Response(serializer.data)