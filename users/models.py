from django.db import models
from django.core.exceptions import ValidationError

# Vérification code pour docteur
def verifier_code_doc(code):
    if not code.endswith("DOC"):
        raise ValidationError("Le code n'est pas valide pour un docteur.")

# Vérification code pour banque
def verifier_code_banc(code):
    if not code.endswith("BANC"):
        raise ValidationError("Le code n'est pas valide pour une banque.")

# Modèle Docteur
class Docteur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    code_inscription = models.CharField(max_length=20, validators=[verifier_code_doc])
    est_verifie = models.BooleanField(default=False)
    BanqueDeSang=models.ForeignKey('BanqueDeSang', on_delete=models.CASCADE, related_name='docteurs', null=True)

    def save(self, *args, **kwargs):
        if self.code_inscription.endswith("DOC"):
            self.est_verifie = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Dr. {self.nom} {self.prenom}"


# Modèle Banque de sang
class BanqueDeSang(models.Model):
    nom = models.CharField(max_length=100)
    localisation = models.CharField(max_length=255)
    code_inscription = models.CharField(max_length=20, validators=[verifier_code_banc])
    est_verifie = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.code_inscription.endswith("BANC"):
            self.est_verifie = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.localisation})"


# Modèle Donneur
class Donneur(models.Model):
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    groupe_sanguin = models.CharField(max_length=5)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.nom} {self.prenom} ({self.groupe_sanguin})"
    



