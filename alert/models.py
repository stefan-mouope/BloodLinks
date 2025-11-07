from django.db import models

class Alerte(models.Model):
    requete = models.ForeignKey('request.Requete', on_delete=models.CASCADE, related_name='alertes')
    date_envoi = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En attente'),('envoyee', 'Envoyée'), ('acceptee', 'Acceptée'), ('annulee', 'Annulée')],
        default='envoyee'
    )

    def __str__(self):
        return f"Alerte {self.id} ({self.statut})"



class RecevoirAlerte(models.Model):
    alerte = models.ForeignKey('alert.Alerte', on_delete=models.CASCADE, related_name='recus')
    donneur = models.ForeignKey('users.Donneur', on_delete=models.CASCADE, related_name='recus')
    date_reception = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente','En attente'),('accepte','Accepté'),('refuse','Refusé')],
        default='en_attente'
    )

    def __str__(self):
        return f"{self.donneur} -> Alerte {self.alerte.id}"
