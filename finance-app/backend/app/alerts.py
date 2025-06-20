from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.services.alert import AlertService
from app.schemas.schemas import Alert, AlertCreate, AlertUpdate
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=Alert, status_code=status.HTTP_201_CREATED)
async def create_alert(
    alert: AlertCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Crée une nouvelle alerte pour l'utilisateur connecté.
    """
    return await AlertService.create_alert(db, alert, current_user["id"])

@router.get("/", response_model=List[Alert])
async def read_alerts(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Récupère toutes les alertes de l'utilisateur connecté.
    """
    return await AlertService.get_alerts(db, current_user["id"])

@router.get("/{alert_id}", response_model=Alert)
async def read_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Récupère une alerte spécifique de l'utilisateur connecté.
    """
    alert = await AlertService.get_alert(db, alert_id, current_user["id"])
    if not alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerte non trouvée"
        )
    return alert

@router.put("/{alert_id}", response_model=Alert)
async def update_alert(
    alert_id: int,
    alert_update: AlertUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Met à jour une alerte existante de l'utilisateur connecté.
    """
    updated_alert = await AlertService.update_alert(db, alert_id, alert_update, current_user["id"])
    if not updated_alert:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerte non trouvée"
        )
    return updated_alert

@router.delete("/{alert_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Supprime une alerte de l'utilisateur connecté.
    """
    success = await AlertService.delete_alert(db, alert_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Alerte non trouvée"
        )
    return {"status": "success"}
