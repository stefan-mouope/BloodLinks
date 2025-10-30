from django.shortcuts import render

# Create your views here.
from users.models import BanqueDeSang

from rest_framework import generics, permissions
from .serializers import BanqueDeSangSerializer

class BanqueDeSangListView(generics.ListAPIView):
    """
    Liste toutes les banques de sang
    """
    queryset = BanqueDeSang.objects.all()
    serializer_class = BanqueDeSangSerializer
    permission_classes = [permissions.AllowAny]  # accessible à tous


class BanqueDeSangDetailView(generics.RetrieveAPIView):
    """
    Récupère les infos d'une banque spécifique par ID
    """
    queryset = BanqueDeSang.objects.all()
    serializer_class = BanqueDeSangSerializer
    permission_classes = [permissions.AllowAny]
