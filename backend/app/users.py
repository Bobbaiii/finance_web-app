from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.services.user import UserService
from app.schemas.schemas import User, UserCreate, Token, NotificationSetting, NotificationSettingCreate, NotificationSettingUpdate
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db)
):
    """
    Enregistre un nouvel utilisateur.
    """
    db_user = await UserService.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà enregistré"
        )
    return await UserService.create_user(db, user)

@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    """
    Authentifie un utilisateur et retourne un token JWT.
    """
    user = await UserService.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await UserService.create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les informations de l'utilisateur connecté.
    """
    return await UserService.get_user(db, current_user["id"])

@router.get("/notification-settings", response_model=NotificationSetting)
async def get_notification_settings(
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Récupère les paramètres de notification de l'utilisateur connecté.
    """
    settings = await UserService.get_notification_settings(db, current_user["id"])
    if not settings:
        # Créer des paramètres par défaut si aucun n'existe
        settings_create = NotificationSettingCreate(user_id=current_user["id"])
        settings = await UserService.create_notification_settings(db, settings_create)
    return settings

@router.put("/notification-settings", response_model=NotificationSetting)
async def update_notification_settings(
    settings_update: NotificationSettingUpdate,
    current_user: Dict[str, Any] = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Met à jour les paramètres de notification de l'utilisateur connecté.
    """
    settings = await UserService.get_notification_settings(db, current_user["id"])
    if not settings:
        # Créer des paramètres par défaut si aucun n'existe
        settings_create = NotificationSettingCreate(
            user_id=current_user["id"],
            **settings_update.dict(exclude_unset=True)
        )
        return await UserService.create_notification_settings(db, settings_create)
    
    return await UserService.update_notification_settings(db, current_user["id"], settings_update)
