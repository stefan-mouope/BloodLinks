import os
import django

# ⚙️ Adapter le nom de ton projet ici (le dossier contenant settings.py)
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'BloodLinks.settings')
django.setup()

from users.models import Docteur, Donneur, BanqueDeSang

# Supprimer d'anciennes données (optionnel)
Docteur.objects.all().delete()
Donneur.objects.all().delete()
BanqueDeSang.objects.all().delete()

# 🏥 Créer une banque de sang
b1 = BanqueDeSang.objects.create(
    nom="Banque Hôpital Général",
    localisation="Douala",
    code_inscription="1234BANC"
)

b2 = BanqueDeSang.objects.create(
    nom="Banque de Sang Laquintinie",
    localisation="Yaoundé",
    code_inscription="5678BANC"
)

# 👨‍⚕️ Créer quelques docteurs
d1 = Docteur.objects.create(
    nom="Mouope",
    prenom="Stefan",
    code_inscription="1111DOC"
)

d2 = Docteur.objects.create(
    nom="Ngongang",
    prenom="Samuel",
    code_inscription="2222DOC"
)

d3 = Docteur.objects.create(
    nom="Tchouameni",
    prenom="Roland",
    code_inscription="3333DOC"
)

# 🩸 Créer quelques donneurs
donneur1 = Donneur.objects.create(
    nom="Bouognong",
    prenom="Stefan",
    groupe_sanguin="A+"
)

donneur2 = Donneur.objects.create(
    nom="Kouam",
    prenom="Elise",
    groupe_sanguin="O-"
)

donneur3 = Donneur.objects.create(
    nom="Talla",
    prenom="Franck",
    groupe_sanguin="B+"
)

print("✅ Données de test créées avec succès :")
print(f"- Banques : {BanqueDeSang.objects.count()}")
print(f"- Docteurs : {Docteur.objects.count()}")
print(f"- Donneurs : {Donneur.objects.count()}")
