from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from app.db.session import get_db
from app.services.portfolio import PortfolioService
from app.schemas.schemas import Portfolio, PortfolioCreate, PortfolioUpdate, Transaction, TransactionCreate, Asset
from app.api.deps import get_current_user

router = APIRouter()

@router.post("/", response_model=Portfolio, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Crée un nouveau portefeuille pour l'utilisateur connecté.
    """
    return await PortfolioService.create_portfolio(db, portfolio, current_user["id"])

@router.get("/", response_model=List[Portfolio])
async def read_portfolios(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Récupère tous les portefeuilles de l'utilisateur connecté.
    """
    return await PortfolioService.get_portfolios(db, current_user["id"])

@router.get("/{portfolio_id}", response_model=Portfolio)
async def read_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Récupère un portefeuille spécifique de l'utilisateur connecté.
    """
    portfolio = await PortfolioService.get_portfolio(db, portfolio_id, current_user["id"])
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille non trouvé"
        )
    return portfolio

@router.put("/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Met à jour un portefeuille existant de l'utilisateur connecté.
    """
    updated_portfolio = await PortfolioService.update_portfolio(db, portfolio_id, portfolio_update, current_user["id"])
    if not updated_portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille non trouvé"
        )
    return updated_portfolio

@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Supprime un portefeuille de l'utilisateur connecté.
    """
    success = await PortfolioService.delete_portfolio(db, portfolio_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille non trouvé"
        )
    return {"status": "success"}

@router.post("/{portfolio_id}/transactions", response_model=Transaction)
async def add_transaction(
    portfolio_id: int,
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Ajoute une transaction à un portefeuille de l'utilisateur connecté.
    """
    # Vérifier que le portfolio_id dans le chemin correspond à celui dans la transaction
    if transaction.portfolio_id != portfolio_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="L'ID du portefeuille dans le chemin ne correspond pas à celui dans la transaction"
        )
    
    new_transaction = await PortfolioService.add_transaction(db, transaction, current_user["id"])
    if not new_transaction:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille ou actif non trouvé"
        )
    return new_transaction

@router.get("/{portfolio_id}/performance")
async def get_portfolio_performance(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Calcule les performances d'un portefeuille de l'utilisateur connecté.
    """
    performance = await PortfolioService.get_portfolio_performance(db, portfolio_id, current_user["id"])
    if "error" in performance:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=performance["error"]
        )
    return performance

@router.post("/favorites/{asset_id}")
async def add_to_favorites(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Ajoute un actif aux favoris de l'utilisateur connecté.
    """
    success = await PortfolioService.add_asset_to_favorites(db, asset_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur ou actif non trouvé"
        )
    return {"status": "success"}

@router.delete("/favorites/{asset_id}")
async def remove_from_favorites(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Retire un actif des favoris de l'utilisateur connecté.
    """
    success = await PortfolioService.remove_asset_from_favorites(db, asset_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Utilisateur ou actif non trouvé"
        )
    return {"status": "success"}

@router.get("/favorites", response_model=List[Asset])
async def get_favorites(
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Récupère les actifs favoris de l'utilisateur connecté.
    """
    return await PortfolioService.get_favorite_assets(db, current_user["id"])
