from django.db import models

class Alerte(models.Model):
    requete = models.ForeignKey('request.Requete', on_delete=models.CASCADE, related_name='alertes')
    date_envoi = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('envoyee', 'Envoyée'), ('acceptee', 'Acceptée'), ('annulee', 'Annulée')],
        default='envoyee'
    )

    def __str__(self):
        return f"Alerte {self.id} ({self.statut})"
