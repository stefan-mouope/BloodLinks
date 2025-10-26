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
    """
    Envoie une notification FCM à un ou plusieurs appareils.
    :param tokens: liste de tokens FCM (ou un seul token string)
    :param title: titre de la notification
    :param body: corps du message
    :param data: dictionnaire optionnel de données supplémentaires
    """

    # Si un seul token est passé, on le met dans une liste
    if isinstance(tokens, str):
        tokens = [tokens]

    # Construire le message multicast
    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body,
        ),
        data=data or {},
        tokens=tokens,
    )

    try:
        # Envoi de la notification
        response = messaging.send_multicast(message)

        # Afficher les résultats
        print(f"Notifications envoyées : {response.success_count} réussies / {response.failure_count} échecs")

        # Gérer les erreurs individuelles
        if response.failure_count > 0:
            for idx, resp in enumerate(response.responses):
                if not resp.success:
                    print(f"Échec pour le token {tokens[idx]} : {resp.exception}")

        return response.success_count > 0

    except Exception as e:
        print(f"Erreur lors de l'envoi des notifications : {e}")
        return False