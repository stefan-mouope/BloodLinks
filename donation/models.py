from django.db import models

class Don(models.Model):
    banque = models.ForeignKey('users.BanqueDeSang', on_delete=models.CASCADE, related_name='dons')
    alerte = models.ForeignKey('alert.Alerte', on_delete=models.CASCADE, related_name='dons')
    donneur = models.ForeignKey('users.Donneur', on_delete=models.CASCADE, related_name='dons')
    date_don = models.DateTimeField(auto_now_add=True)
    statut = models.CharField(
        max_length=20,
        choices=[('en_attente', 'En attente'), ('valide', 'Validé'), ('annule', 'Annulé')],
        default='en_attente'
    )

    def __str__(self):
        return f"Don {self.id} - {self.donneur} ({self.statut})"


