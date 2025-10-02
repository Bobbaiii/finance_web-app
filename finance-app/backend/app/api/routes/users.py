from typing import Dict

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import deps
from app.db.session import get_db
from app.schemas import (
    NotificationSetting,
    NotificationSettingCreate,
    NotificationSettingUpdate,
    Token,
    User,
    UserCreate,
)
from app.services.user import UserService

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
async def register_user(
    user: UserCreate,
    db: Session = Depends(get_db),
) -> User:
    """Enregistrer un nouvel utilisateur."""
    db_user = await UserService.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email déjà enregistré",
        )
    return await UserService.create_user(db, user)


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
) -> Token:
    """Authentifier un utilisateur et retourner un token JWT."""
    user = await UserService.authenticate_user(
        db, form_data.username, form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou mot de passe incorrect",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = await UserService.create_access_token(data={"sub": str(user.id)})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/me", response_model=User)
async def read_users_me(
    current_user: Dict[str, int] = Depends(deps.get_current_user),
    db: Session = Depends(get_db),
) -> User:
    """Récupérer les informations de l'utilisateur connecté."""
    return await UserService.get_user(db, current_user["id"])


@router.get("/notification-settings", response_model=NotificationSetting)
async def get_notification_settings(
    current_user: Dict[str, int] = Depends(deps.get_current_user),
    db: Session = Depends(get_db),
) -> NotificationSetting:
    """Récupérer les paramètres de notification de l'utilisateur connecté."""
    settings = await UserService.get_notification_settings(db, current_user["id"])
    if not settings:
        settings_create = NotificationSettingCreate(user_id=current_user["id"])
        settings = await UserService.create_notification_settings(db, settings_create)
    return settings


@router.put("/notification-settings", response_model=NotificationSetting)
async def update_notification_settings(
    settings_update: NotificationSettingUpdate,
    current_user: Dict[str, int] = Depends(deps.get_current_user),
    db: Session = Depends(get_db),
) -> NotificationSetting:
    """Mettre à jour les paramètres de notification de l'utilisateur connecté."""
    settings = await UserService.get_notification_settings(db, current_user["id"])
    if not settings:
        settings_create = NotificationSettingCreate(
            user_id=current_user["id"],
            **settings_update.dict(exclude_unset=True),
        )
        return await UserService.create_notification_settings(db, settings_create)

    updated_settings = await UserService.update_notification_settings(
        db, current_user["id"], settings_update
    )
    if not updated_settings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paramètres de notification non trouvés",
        )
    return updated_settings
