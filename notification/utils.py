# notification/utils.py
from firebase_admin import messaging
from config.firebase_config import firebase_admin
from django.contrib.auth import get_user_model
from notification.models import FCMToken  # à adapter selon ton modèle
from django.core.exceptions import ObjectDoesNotExist
from users.models import Docteur
User = get_user_model()

def send_push_notification(token, title, body, data=None):
    """
    Envoie une notification FCM à un appareil spécifique.
    """
    message = messaging.Message(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        token=token,
    )

    try:
        response = messaging.send(message)
        print(f"✅ Notification envoyée avec succès : {response}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi de la notification : {e}")
        return False


def send_multicast_push_notification(tokens, title, body, data=None):
    """
    Envoie une notification à plusieurs tokens.
    """
    if isinstance(tokens, str):
        tokens = [tokens]

    success_count = 0
    for token in tokens:
        message = messaging.Message(
            notification=messaging.Notification(title=title, body=body),
            data=data or {},
            token=token,
        )
        try:
            messaging.send(message)
            success_count += 1
        except Exception as e:
            print(f"⚠️ Échec pour le token {token}: {e}")
    print(f"notification envoyées : {success_count} réussies / {len(tokens) - success_count} échecs")
    return success_count > 0


def send_notification_to_user(user_id, title, body, data=None):
    """
    🔹 Récupère le token FCM d’un utilisateur et lui envoie une notification.
    """
    try:
        # Récupère l'utilisateur
        user = User.objects.get(id=user_id)

        # Récupère son token (à adapter selon ton modèle)
        device = FCMToken.objects.filter(user=user).last()

        if not device or not device.token:
            print(f"⚠️ Aucun token trouvé pour l'utilisateur {user_id}")
            return False

        # Envoie la notification
        return send_push_notification(device.token, title, body, data)

    except ObjectDoesNotExist:
        print(f"❌ Utilisateur avec id={user_id} introuvable")
        return False
    except Exception as e:
        print(f"❌ Erreur lors de l'envoi au user {user_id} : {e}")
        return False


def send_notification_to_banque(banque_id, title, body, data=None):
    """
    Envoie une notification à la banque de sang donnée.
    Tous les docteurs rattachés à cette banque recevront la notification.
    """


    docteurs = Docteur.objects.filter(BanqueDeSang_id=banque_id)
    tokens = []

    for doc in docteurs:
        device = FCMToken.objects.filter(user=doc.user).first()
        if device and device.token:
            tokens.append(device.token)

    if not tokens:
        print(f"Aucun token trouvé pour la banque de sang {banque_id}")
        return False

    for token in tokens:
        try:
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body,
                ),
                data=data or {},
                token=token,
            )
            messaging.send(message)
            print(f"Notification envoyée à un docteur de la banque {banque_id}")
        except Exception as e:
            print(f"Erreur lors de l'envoi à la banque {banque_id} : {e}")
    return True
