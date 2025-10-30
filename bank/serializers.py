from rest_framework import serializers
from users.models import BanqueDeSang

class BanqueDeSangSerializer(serializers.ModelSerializer):
    """
    Sérialiseur pour le modèle BanqueDeSang
    """
    email = serializers.EmailField(source='user.email', read_only=True)  # pour afficher l'email du user lié

    class Meta:
        model = BanqueDeSang
        fields = ['id', 'nom', 'localisation', 'code_inscription', 'est_verifie', 'email']
