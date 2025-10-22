from rest_framework import viewsets
from .models import Requete
from .serializers import RequeteSerializer

class RequeteViewSet(viewsets.ModelViewSet):
    queryset = Requete.objects.all()
    serializer_class = RequeteSerializer
