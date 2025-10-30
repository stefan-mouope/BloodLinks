from rest_framework import serializers
from .models import Requete
from users.models import Docteur



class DocteurInfoSerializer(serializers.ModelSerializer):
    BanqueDeSang_id = serializers.IntegerField(source='BanqueDeSang.id', read_only=True)
    BanqueDeSang_nom = serializers.CharField(source='BanqueDeSang.nom', read_only=True)

    class Meta:
        model = Docteur
        fields = ['nom', 'prenom', 'code_inscription', 'est_verifie', 'BanqueDeSang_id', 'BanqueDeSang_nom']



class RequeteSerializer(serializers.ModelSerializer):
    docteur = DocteurInfoSerializer(read_only=True)

    class Meta:
        model = Requete
        fields = ['id', 'date_requete', 'groupe_sanguin','quantite', 'statut', 'docteur']

