from typing import Dict, List

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app import deps
from app.db.session import get_db
from app.schemas import (
    Portfolio,
    PortfolioCreate,
    PortfolioUpdate,
    Transaction,
    TransactionCreate,
)
from app.services.portfolio import PortfolioService

router = APIRouter()


@router.post("/", response_model=Portfolio, status_code=status.HTTP_201_CREATED)
async def create_portfolio(
    portfolio: PortfolioCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Portfolio:
    """Créer un nouveau portefeuille pour l'utilisateur connecté."""
    return await PortfolioService.create_portfolio(db, portfolio, current_user["id"])


@router.get("/", response_model=List[Portfolio])
async def read_portfolios(
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> List[Portfolio]:
    """Récupérer les portefeuilles de l'utilisateur connecté."""
    return await PortfolioService.get_portfolios(db, current_user["id"])


@router.get("/{portfolio_id}", response_model=Portfolio)
async def read_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Portfolio:
    """Récupérer un portefeuille précis de l'utilisateur connecté."""
    portfolio = await PortfolioService.get_portfolio(db, portfolio_id, current_user["id"])
    if not portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille non trouvé",
        )
    return portfolio


@router.put("/{portfolio_id}", response_model=Portfolio)
async def update_portfolio(
    portfolio_id: int,
    portfolio_update: PortfolioUpdate,
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Portfolio:
    """Mettre à jour un portefeuille existant."""
    updated_portfolio = await PortfolioService.update_portfolio(
        db, portfolio_id, portfolio_update, current_user["id"]
    )
    if not updated_portfolio:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille non trouvé",
        )
    return updated_portfolio


@router.delete("/{portfolio_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_portfolio(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Response:
    """Supprimer un portefeuille de l'utilisateur connecté."""
    success = await PortfolioService.delete_portfolio(db, portfolio_id, current_user["id"])
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille non trouvé",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/transactions",
    response_model=Transaction,
    status_code=status.HTTP_201_CREATED,
)
async def add_transaction(
    transaction: TransactionCreate,
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Transaction:
    """Ajouter une transaction à un portefeuille."""
    new_transaction = await PortfolioService.add_transaction(
        db, transaction, current_user["id"]
    )
    if not new_transaction:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Impossible d'ajouter la transaction",
        )
    return new_transaction


@router.get("/{portfolio_id}/performance")
async def get_portfolio_performance(
    portfolio_id: int,
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Dict[str, object]:
    """Obtenir les métriques de performance d'un portefeuille."""
    performance = await PortfolioService.get_portfolio_performance(
        db, portfolio_id, current_user["id"]
    )
    if performance is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Portefeuille non trouvé",
        )
    return performance
