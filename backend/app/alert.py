from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.models import Alert, User, Asset, NotificationSetting
from app.schemas.schemas import AlertCreate, AlertUpdate
from datetime import datetime
import aiohttp
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings

class AlertService:
    """
    Service pour la gestion des alertes et des notifications.
    """
    
    @staticmethod
    async def create_alert(db: Session, alert: AlertCreate, user_id: int) -> Alert:
        """
        Crée une nouvelle alerte pour un utilisateur.
        
        Args:
            db: Session de base de données
            alert: Données de l'alerte à créer
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            L'alerte créée
        """
        db_alert = Alert(
            user_id=user_id,
            asset_id=alert.asset_id,
            alert_type=alert.alert_type,
            condition=alert.condition,
            value=alert.value,
            is_active=alert.is_active,
            is_repeatable=alert.is_repeatable
        )
        db.add(db_alert)
        db.commit()
        db.refresh(db_alert)
        return db_alert
    
    @staticmethod
    async def get_alerts(db: Session, user_id: int) -> List[Alert]:
        """
        Récupère toutes les alertes d'un utilisateur.
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            
        Returns:
            Liste des alertes de l'utilisateur
        """
        return db.query(Alert).filter(Alert.user_id == user_id).all()
    
    @staticmethod
    async def get_alert(db: Session, alert_id: int, user_id: int) -> Optional[Alert]:
        """
        Récupère une alerte spécifique d'un utilisateur.
        
        Args:
            db: Session de base de données
            alert_id: ID de l'alerte
            user_id: ID de l'utilisateur
            
        Returns:
            L'alerte si elle existe et appartient à l'utilisateur, None sinon
        """
        return db.query(Alert).filter(
            Alert.id == alert_id,
            Alert.user_id == user_id
        ).first()
    
    @staticmethod
    async def update_alert(
        db: Session, 
        alert_id: int, 
        alert_update: AlertUpdate, 
        user_id: int
    ) -> Optional[Alert]:
        """
        Met à jour une alerte existante.
        
        Args:
            db: Session de base de données
            alert_id: ID de l'alerte à mettre à jour
            alert_update: Données de mise à jour
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            L'alerte mise à jour si elle existe et appartient à l'utilisateur, None sinon
        """
        db_alert = await AlertService.get_alert(db, alert_id, user_id)
        if not db_alert:
            return None
        
        update_data = alert_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_alert, key, value)
        
        db.commit()
        db.refresh(db_alert)
        return db_alert
    
    @staticmethod
    async def delete_alert(db: Session, alert_id: int, user_id: int) -> bool:
        """
        Supprime une alerte.
        
        Args:
            db: Session de base de données
            alert_id: ID de l'alerte à supprimer
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            True si l'alerte a été supprimée, False sinon
        """
        db_alert = await AlertService.get_alert(db, alert_id, user_id)
        if not db_alert:
            return False
        
        db.delete(db_alert)
        db.commit()
        return True
    
    @staticmethod
    async def check_alerts(db: Session) -> List[Dict[str, Any]]:
        """
        Vérifie toutes les alertes actives et déclenche les notifications si nécessaire.
        
        Args:
            db: Session de base de données
            
        Returns:
            Liste des alertes déclenchées
        """
        # Récupérer toutes les alertes actives
        active_alerts = db.query(Alert).filter(Alert.is_active == True).all()
        triggered_alerts = []
        
        for alert in active_alerts:
            # Récupérer l'actif associé à l'alerte
            asset = db.query(Asset).filter(Asset.id == alert.asset_id).first()
            if not asset or not asset.last_price:
                continue
            
            # Vérifier si l'alerte doit être déclenchée
            should_trigger = False
            
            if alert.alert_type == "price":
                if alert.condition == "above" and asset.last_price > alert.value:
                    should_trigger = True
                elif alert.condition == "below" and asset.last_price < alert.value:
                    should_trigger = True
                elif alert.condition == "equals" and abs(asset.last_price - alert.value) < 0.001:
                    should_trigger = True
            
            # Pour les autres types d'alertes (ICT, indicateurs), des vérifications spécifiques seraient nécessaires
            # Cela nécessiterait d'intégrer le service d'analyse technique
            
            if should_trigger:
                # Récupérer l'utilisateur et ses préférences de notification
                user = db.query(User).filter(User.id == alert.user_id).first()
                notification_settings = db.query(NotificationSetting).filter(
                    NotificationSetting.user_id == alert.user_id
                ).first()
                
                if user and notification_settings:
                    # Préparer le message de notification
                    message = f"Alerte: {asset.symbol} {alert.condition} {alert.value}"
                    
                    # Envoyer les notifications selon les préférences de l'utilisateur
                    if notification_settings.email_enabled:
                        await AlertService.send_email_notification(user.email, message)
                    
                    if notification_settings.telegram_enabled and notification_settings.telegram_chat_id:
                        await AlertService.send_telegram_notification(
                            notification_settings.telegram_chat_id, 
                            message
                        )
                    
                    if notification_settings.whatsapp_enabled and notification_settings.whatsapp_number:
                        await AlertService.send_whatsapp_notification(
                            notification_settings.whatsapp_number, 
                            message
                        )
                
                # Mettre à jour la date de déclenchement de l'alerte
                alert.last_triggered = datetime.now()
                
                # Désactiver l'alerte si elle n'est pas répétable
                if not alert.is_repeatable:
                    alert.is_active = False
                
                db.commit()
                
                triggered_alerts.append({
                    "alert_id": alert.id,
                    "user_id": alert.user_id,
                    "asset_symbol": asset.symbol,
                    "alert_type": alert.alert_type,
                    "condition": alert.condition,
                    "value": alert.value,
                    "current_price": asset.last_price,
                    "triggered_at": alert.last_triggered
                })
        
        return triggered_alerts
    
    @staticmethod
    async def send_email_notification(email: str, message: str) -> bool:
        """
        Envoie une notification par email.
        
        Args:
            email: Adresse email du destinataire
            message: Contenu de la notification
            
        Returns:
            True si l'email a été envoyé avec succès, False sinon
        """
        try:
            # Configurer le message
            msg = MIMEMultipart()
            msg['From'] = settings.EMAIL_USERNAME
            msg['To'] = email
            msg['Subject'] = "Alerte Finance App"
            
            # Ajouter le corps du message
            msg.attach(MIMEText(message, 'plain'))
            
            # Établir la connexion au serveur SMTP
            server = smtplib.SMTP(settings.EMAIL_HOST, settings.EMAIL_PORT)
            server.starttls()
            server.login(settings.EMAIL_USERNAME, settings.EMAIL_PASSWORD)
            
            # Envoyer l'email
            server.send_message(msg)
            server.quit()
            
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi de l'email: {str(e)}")
            return False
    
    @staticmethod
    async def send_telegram_notification(chat_id: str, message: str) -> bool:
        """
        Envoie une notification via Telegram.
        
        Args:
            chat_id: ID du chat Telegram
            message: Contenu de la notification
            
        Returns:
            True si le message a été envoyé avec succès, False sinon
        """
        try:
            # URL de l'API Telegram pour envoyer un message
            url = f"https://api.telegram.org/bot{settings.TELEGRAM_BOT_TOKEN}/sendMessage"
            
            # Paramètres du message
            params = {
                "chat_id": chat_id,
                "text": message
            }
            
            # Envoyer la requête à l'API Telegram
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=params) as response:
                    return response.status == 200
        except Exception as e:
            print(f"Erreur lors de l'envoi de la notification Telegram: {str(e)}")
            return False
    
    @staticmethod
    async def send_whatsapp_notification(phone_number: str, message: str) -> bool:
        """
        Envoie une notification via WhatsApp.
        
        Note: Cette implémentation est simplifiée et nécessiterait l'intégration
        avec l'API WhatsApp Business ou un service tiers comme Twilio.
        
        Args:
            phone_number: Numéro de téléphone du destinataire
            message: Contenu de la notification
            
        Returns:
            True si le message a été envoyé avec succès, False sinon
        """
        try:
            # Cette implémentation est un placeholder
            # Dans une application réelle, il faudrait intégrer l'API WhatsApp Business
            # ou utiliser un service tiers comme Twilio
            
            print(f"Envoi d'une notification WhatsApp à {phone_number}: {message}")
            
            # Simuler un succès pour l'exemple
            return True
        except Exception as e:
            print(f"Erreur lors de l'envoi de la notification WhatsApp: {str(e)}")
            return False
