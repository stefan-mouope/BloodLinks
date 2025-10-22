from django.db import models

# Ici, on fait juste référence à la BanqueDeSang du dev1
# FK pointant vers users.BanqueDeSang

class BanqueOperation(models.Model):
    banque = models.ForeignKey('users.BanqueDeSang', on_delete=models.CASCADE, related_name='operations')
    # Type d'opération : envoi d'alerte, validation de don, annulation d'alerte
    type_operation = models.CharField(
        max_length=50,
        choices=[
            ('envoi_alerte', 'Envoi Alerte'),
            ('valide_don', 'Valide Don'),
            ('cancel_alerte', 'Annule Alerte')
        ]
    )
    date_operation = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)

    def __str__(self):
        return f"{self.banque.nom} - {self.type_operation} ({self.date_operation})"
