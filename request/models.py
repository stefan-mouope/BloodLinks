from django.db import models

class Requete(models.Model):
    docteur = models.ForeignKey('users.Docteur', on_delete=models.CASCADE, related_name='requetes')
    date_requete = models.DateTimeField(auto_now_add=True)
    groupe_sanguin = models.CharField(max_length=5)
    quantite = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"Requete {self.id} - {self.groupe_sanguin}"
