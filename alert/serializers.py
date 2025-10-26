from rest_framework import serializers, status
from rest_framework.response import  Response
from .models import Alerte, RecevoirAlerte
from users.models import Donneur
from notifications.utils import send_multicast_push_notification
from notifications.models import FCMToken

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
    groupe_sanguin = serializers.CharField(write_only=True)
    donneurs = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Alerte
        fields = ['id', 'requete', 'date_envoi', 'statut', 'groupe_sanguin', 'donneurs']

    def create(self, validated_data):
        groupe = validated_data.pop('groupe_sanguin')
        alerte = Alerte.objects.create(**validated_data)

        # 🔹 Étape 1 : trouver les donneurs correspondants
        donneurs = Donneur.objects.filter(groupe_sanguin=groupe)

        # 🔹 Étape 2 : créer les entrées RecevoirAlerte
        for donneur in donneurs:
            RecevoirAlerte.objects.create(alerte=alerte, donneur=donneur)

        # 🔹 Étape 3 : récupérer les tokens FCM des donneurs
        tokens = list(
            FCMToken.objects.filter(user__in=[d.user for d in donneurs])
            .values_list("token", flat=True)
        )

        # 🔹 Étape 4 : envoyer la notification
        if tokens:
            title = "Nouvelle alerte de don de sang"
            body = f"Une banque de sang a besoin de votre groupe {groupe}"
            data = {"alerte_id": str(alerte.id), "groupe": groupe}

            send_multicast_push_notification(tokens, title, body, data)

        return alerte

    def get_donneurs(self, obj):
        recu_qs = obj.recus.all()  # relation related_name='recus'
        donneurs = [r.donneur for r in recu_qs]
        return DonneurMiniSerializer(donneurs, many=True).data