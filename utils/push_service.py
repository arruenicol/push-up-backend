import json
import requests
from django.conf import settings
import firebase_admin
from firebase_admin import credentials, messaging


class FirebasePushService:
    """Clase para enviar notificaciones push usando Firebase Cloud Messaging"""
    
    def __init__(self):
        # Inicializar Firebase Admin SDK
        if not firebase_admin._apps:
            cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
            firebase_admin.initialize_app(cred)
    
    def send_notification(self, token, title, body, data=None):
        """
        Envía una notificación push a un dispositivo específico
        
        Args:
            token (str): Token de dispositivo FCM
            title (str): Título de la notificación
            body (str): Cuerpo de la notificación
            data (dict, optional): Datos adicionales para la notificación
        
        Returns:
            str: ID del mensaje enviado
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
            return response
        except Exception as e:
            print(f"Error sending notification: {e}")
            return None
    
    def send_multicast(self, tokens, title, body, data=None):
        """
        Envía una notificación push a múltiples dispositivos
        
        Args:
            tokens (list): Lista de tokens de dispositivo FCM
            title (str): Título de la notificación
            body (str): Cuerpo de la notificación
            data (dict, optional): Datos adicionales para la notificación
        
        Returns:
            messaging.BatchResponse: Respuesta del envío por lotes
        """
        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            data=data or {},
            tokens=tokens,
        )
        
        try:
            response = messaging.send_multicast(message)
            return response
        except Exception as e:
            print(f"Error sending multicast notification: {e}")
            return None


# Función helper para otras partes de la aplicación
def send_push_notification(token, title, body, data=None):
    """
    Función helper para enviar notificación push
    
    Args:
        token (str): Token de dispositivo FCM
        title (str): Título de la notificación
        body (str): Cuerpo de la notificación
        data (dict, optional): Datos adicionales para la notificación
    """
    service = FirebasePushService()
    return service.send_notification(token, title, body, data)


def send_multicast_push_notification(tokens, title, body, data=None):
    """
    Función helper para enviar notificación push a múltiples dispositivos
    
    Args:
        tokens (list): Lista de tokens de dispositivo FCM
        title (str): Título de la notificación
        body (str): Cuerpo de la notificación
        data (dict, optional): Datos adicionales para la notificación
    """
    service = FirebasePushService()
    return service.send_multicast(tokens, title, body, data)