from rest_framework import serializers, status
from rest_framework.response import  Response
from .models import Alerte, RecevoirAlerte
from users.models import Donneur

class DonneurMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donneur
        fields = ['id', 'nom', 'prenom', 'groupe_sanguin']

class RecevoirAlerteSerializer(serializers.ModelSerializer):
    donneur = DonneurMiniSerializer(read_only=True)

    class Meta:
        model = RecevoirAlerte
        fields = ['id', 'alerte', 'donneur', 'date_reception', 'statut']


class AlerteSerializer(serializers.ModelSerializer):
    groupe_sanguin = serializers.CharField(write_only=True)  # pour filtrer les donneurs
    donneurs = serializers.SerializerMethodField(read_only=True)  # pour retourner les donneurs

    class Meta:
        model = Alerte
        fields = ['id', 'requete', 'date_envoi', 'statut', 'groupe_sanguin', 'donneurs']

    def create(self, validated_data):
        groupe = validated_data.pop('groupe_sanguin')
        alerte = Alerte.objects.create(**validated_data)

        # Récupérer les donneurs correspondant au groupe sanguin
        donneurs = Donneur.objects.filter(groupe_sanguin=groupe)

        # Créer les entrées RecevoirAlerte
        for d in donneurs:
            RecevoirAlerte.objects.create(alerte=alerte, donneur=d)

        return alerte

    def get_donneurs(self, obj):
        recu_qs = obj.recus.all()  # relation related_name='recus'
        return DonneurMiniSerializer([r.donneur for r in recu_qs], many=True).data
