from rest_framework import viewsets, status
from rest_framework.response import Response
from .models import Don, FaireDon
from .serializers import DonSerializer, FaireDonSerializer

class FaireDonViewSet(viewsets.ModelViewSet):
    queryset = FaireDon.objects.all()
    serializer_class = FaireDonSerializer


class DonViewSet(viewsets.ModelViewSet):
    queryset = Don.objects.all()
    serializer_class = DonSerializer

    # endpoint POST spécial pour "valider" un don
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        new_status = request.data.get('statut', None)
        if new_status and new_status in ['valide', 'annule']:
            instance.statut = new_status
            instance.save()
            return Response(DonSerializer(instance).data, status=status.HTTP_200_OK)
        return Response({"error": "Statut invalide"}, status=status.HTTP_400_BAD_REQUEST)
