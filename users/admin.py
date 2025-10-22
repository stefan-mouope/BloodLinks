from django.contrib import admin
from .models import Docteur, Donneur, BanqueDeSang

@admin.register(Docteur)
class DocteurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'code_inscription', 'est_verifie', 'BanqueDeSang')
    search_fields = ('nom', 'prenom', 'code_inscription', 'BanqueDeSang')

@admin.register(Donneur)
class DonneurAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'groupe_sanguin', 'disponible')
    search_fields = ('nom', 'prenom', 'groupe_sanguin')

@admin.register(BanqueDeSang)
class BanqueAdmin(admin.ModelAdmin):
    list_display = ('id', 'nom', 'localisation', 'code_inscription', 'est_verifie')
    search_fields = ('nom', 'localisation')
