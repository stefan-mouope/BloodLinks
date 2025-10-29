# notifications/utils.py
from firebase_admin import messaging
from config.firebase_config import firebase_admin

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
        print(f"Notification envoyée avec succès : {response}")
        return True
    except Exception as e:
        print(f"Erreur lors de l'envoi de la notification : {e}")
        return False


def send_multicast_push_notification(tokens, title, body, data=None):
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
            print(f"Échec pour le token {token}: {e}")
    print(f"Notifications envoyées : {success_count} réussies / {len(tokens) - success_count} échecs")
    return success_count > 0