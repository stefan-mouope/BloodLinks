from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from .utils import verifier_code_banc, verifier_code_doc
from .manager import CustomUserManager



class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = (
        ('docteur', 'Docteur'),
        ('banque', 'Banque de sang'),
        ('donneur', 'Donneur'),
    )

    email = models.EmailField(unique=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['user_type']

    def __str__(self):
        return self.email


# Modèle Docteur
class Docteur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    code_inscription = models.CharField(max_length=20, validators=[verifier_code_doc])
    est_verifie = models.BooleanField(default=False)
    BanqueDeSang = models.ForeignKey('BanqueDeSang', on_delete=models.CASCADE, related_name='docteurs', null=True)

    def save(self, *args, **kwargs):
        if self.code_inscription.endswith("DOC"):
            self.est_verifie = True
        super().save(*args, **kwargs)



# Modèle Banque de sang
class BanqueDeSang(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=255)
    code_inscription = models.CharField(max_length=20, validators=[verifier_code_banc])
    est_verifie = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.code_inscription.endswith("BANC"):
            self.est_verifie = True
        super().save(*args, **kwargs)



# Modèle Donneur
class Donneur(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='donneurs')
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    groupe_sanguin = models.CharField(max_length=5)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.groupe_sanguin})"



# creer le serializeur le laview pour authitfier les utilisateur avec le jwt ,orsqu'on iscrit un utilisateur on doit le connecter directement on creer un docteur si le  code_iscription fini pas DOC on creer une banque si le code d'inscription fini par BANC , pour un donneur ces inforamtion d'iscription sont son nom,prenom,groupe_ganguin,son email ,son mots de passe  ,pour un docteur on doit avoir nom,prenom,son email,code_d'inscription,la BanqueDeSang ,son mots de passe,et pour une banque on aura nom,son email,code_d'inscription,la BanqueDeSang