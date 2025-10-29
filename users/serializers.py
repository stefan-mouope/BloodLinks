from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Docteur, BanqueDeSang, Donneur

User = get_user_model()


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Sérialiseur personnalisé pour renvoyer les infos de l'utilisateur + tokens
    """
    def validate(self, attrs):
        data = super().validate(attrs)
        user = self.user

        # Infos de base
        user_data = {
            'id': user.id,
            'email': user.email,
            'user_type': user.user_type,
            'is_active': user.is_active,
        }

        # Infos spécifiques selon le type
        if user.user_type == 'donneur' and hasattr(user, 'donneurs'):
            donneur = user.donneurs
            user_data.update({
                'nom': donneur.nom,
                'prenom': donneur.prenom,
                'groupe_sanguin': donneur.groupe_sanguin,
                'disponible': donneur.disponible
            })
        elif user.user_type == 'docteur' and hasattr(user, 'docteur'):
            docteur = user.docteur
            user_data.update({
                'nom': docteur.nom,
                'prenom': docteur.prenom,
                'code_inscription': docteur.code_inscription,
                'est_verifie': docteur.est_verifie,
                'BanqueDeSang_id': docteur.BanqueDeSang.id if docteur.BanqueDeSang else None,
                'BanqueDeSang_nom': docteur.BanqueDeSang.nom if docteur.BanqueDeSang else None
            })
        elif user.user_type == 'banque' and hasattr(user, 'banquedesang'):
            banque = user.banquedesang
            user_data.update({
                'nom': banque.nom,
                'localisation': banque.localisation,
                'code_inscription': banque.code_inscription,
                'est_verifie': banque.est_verifie
            })

        data['user'] = user_data
        return data


class RegisterSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=User.USER_TYPE_CHOICES)

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

        user = User.objects.create(email=email, user_type=user_type, is_active=True)
        user.set_password(password)
        user.save()

        # Création du profil selon le type
        profile_data = {}
        if user_type == "donneur":
            profile = Donneur.objects.create(user=user, **validated_data)
            profile_data = {
                "nom": profile.nom,
                "prenom": profile.prenom,
                "groupe_sanguin": profile.groupe_sanguin,
                "disponible": profile.disponible
            }

        elif user_type == "docteur":
            profile = Docteur.objects.create(user=user, **validated_data)
            profile_data = {
                "nom": profile.nom,
                "prenom": profile.prenom,
                "code_inscription": profile.code_inscription,
                "est_verifie": profile.est_verifie,
                "BanqueDeSang_id": profile.BanqueDeSang.id if profile.BanqueDeSang else None,
                "BanqueDeSang_nom": profile.BanqueDeSang.nom if profile.BanqueDeSang else None
            }

        elif user_type == "banque":
            profile = BanqueDeSang.objects.create(user=user, **validated_data)
            profile_data = {
                "nom": profile.nom,
                "localisation": profile.localisation,
                "code_inscription": profile.code_inscription,
                "est_verifie": profile.est_verifie
            }

        # Génération du JWT
        refresh = RefreshToken.for_user(user)

        return {
            "id": user.id,
            "email": user.email,
            "user_type": user.user_type,
            "refresh": str(refresh),
            "access": str(refresh.access_token),
            "user": profile_data
        }