from django.db import models

# class Notification(models.Model):
#     user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
#     title = models.CharField(max_length=255)
#     body = models.TextField()
#     statut = models.CharField(max_length=255, choices=[('en_attente', 'En attente'), ('lu', 'Lu')], default='en_attente')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.title

class FCMToken(models.Model):
    user = models.ForeignKey('users.CustomUser', on_delete=models.CASCADE)
    token = models.CharField(max_length=255)
    device_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.token