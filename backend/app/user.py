from typing import Optional, Dict, Any
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.models import User, NotificationSetting
from app.schemas.schemas import UserCreate, NotificationSettingCreate, NotificationSettingUpdate
from app.core.config import settings

# Configuration du hachage des mots de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserService:
    """
    Service pour la gestion des utilisateurs et de l'authentification.
    """
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Vérifie si le mot de passe en clair correspond au mot de passe haché."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def get_password_hash(password: str) -> str:
        """Génère un hash du mot de passe."""
        return pwd_context.hash(password)
    
    @staticmethod
    async def get_user(db: Session, user_id: int) -> Optional[User]:
        """Récupère un utilisateur par son ID."""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    async def get_user_by_email(db: Session, email: str) -> Optional[User]:
        """Récupère un utilisateur par son email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    async def create_user(db: Session, user: UserCreate) -> User:
        """Crée un nouvel utilisateur."""
        hashed_password = UserService.get_password_hash(user.password)
        db_user = User(
            email=user.email,
            hashed_password=hashed_password,
            full_name=user.full_name,
            is_active=user.is_active
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        
        # Créer les paramètres de notification par défaut
        notification_settings = NotificationSetting(
            user_id=db_user.id,
            email_enabled=True,
            telegram_enabled=False,
            whatsapp_enabled=False
        )
        db.add(notification_settings)
        db.commit()
        
        return db_user
    
    @staticmethod
    async def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
        """Authentifie un utilisateur par email et mot de passe."""
        user = await UserService.get_user_by_email(db, email)
        if not user:
            return None
        if not UserService.verify_password(password, user.hashed_password):
            return None
        return user
    
    @staticmethod
    async def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Crée un token JWT pour l'authentification."""
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
    
    @staticmethod
    async def get_notification_settings(db: Session, user_id: int) -> Optional[NotificationSetting]:
        """Récupère les paramètres de notification d'un utilisateur."""
        return db.query(NotificationSetting).filter(NotificationSetting.user_id == user_id).first()
    
    @staticmethod
    async def create_notification_settings(db: Session, settings: NotificationSettingCreate) -> NotificationSetting:
        """Crée les paramètres de notification pour un utilisateur."""
        db_settings = NotificationSetting(
            user_id=settings.user_id,
            email_enabled=settings.email_enabled,
            telegram_enabled=settings.telegram_enabled,
            telegram_chat_id=settings.telegram_chat_id,
            whatsapp_enabled=settings.whatsapp_enabled,
            whatsapp_number=settings.whatsapp_number
        )
        db.add(db_settings)
        db.commit()
        db.refresh(db_settings)
        return db_settings
    
    @staticmethod
    async def update_notification_settings(
        db: Session, 
        user_id: int, 
        settings_update: NotificationSettingUpdate
    ) -> Optional[NotificationSetting]:
        """Met à jour les paramètres de notification d'un utilisateur."""
        db_settings = await UserService.get_notification_settings(db, user_id)
        if not db_settings:
            return None
        
        update_data = settings_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_settings, key, value)
        
        db.commit()
        db.refresh(db_settings)
        return db_settings
