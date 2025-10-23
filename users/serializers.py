from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Docteur, BanqueDeSang, Donneur

User = get_user_model()


class RegisterSerializer(serializers.Serializer):
    # Champs communs
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

    # Champs spécifiques
    nom = serializers.CharField(required=False)
    prenom = serializers.CharField(required=False)
    groupe_sanguin = serializers.CharField(required=False)
    code_inscription = serializers.CharField(required=False)
    localisation = serializers.CharField(required=False)
    BanqueDeSang = serializers.PrimaryKeyRelatedField(
        queryset=BanqueDeSang.objects.all(),
        required=False
    )

    def validate(self, attrs):
        user_type = attrs.get("user_type")

        if user_type == "donneur":
            for field in ["nom", "prenom", "groupe_sanguin"]:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"Le champ '{field}' est obligatoire pour un donneur.")
        
        elif user_type == "docteur":
            for field in ["nom", "prenom", "code_inscription", "BanqueDeSang"]:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"Le champ '{field}' est obligatoire pour un docteur.")
            if not attrs["code_inscription"].endswith("DOC"):
                raise serializers.ValidationError("Le code d'inscription du docteur doit se terminer par 'DOC'.")
        
        elif user_type == "banque":
            for field in ["nom", "localisation", "code_inscription"]:
                if not attrs.get(field):
                    raise serializers.ValidationError(f"Le champ '{field}' est obligatoire pour une banque.")
            if not attrs["code_inscription"].endswith("BANC"):
                raise serializers.ValidationError("Le code d'inscription de la banque doit se terminer par 'BANC'.")
        
        return attrs

    def create(self, validated_data):
        user_type = validated_data.pop("user_type")
        password = validated_data.pop("password")
        email = validated_data.pop("email")

        # Création de l'utilisateur principal
        user = User.objects.create(email=email, user_type=user_type)
        user.set_password(password)
        user.save()

        # Création du profil selon le type
        if user_type == "donneur":
            Donneur.objects.create(user=user, **validated_data)
            refresh = RefreshToken.for_user(user)
            return {
            "id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        elif user_type == "docteur":
            Docteur.objects.create(user=user, **validated_data)
        elif user_type == "banque":
            BanqueDeSang.objects.create(user=user, **validated_data)

        # Génération du JWT
        

        # Retourne un dict avec uniquement des données sérialisables
        return {
            "id": user.id,
            "email": user.email,
            "user_type": user.user_type,
        }


    def to_representation(self, instance):
        """Format du retour après inscription"""
        user = instance["user"]
        return {
            "id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "refresh": instance["refresh"],
            "access": instance["access"],
        }
