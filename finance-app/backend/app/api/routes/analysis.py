from typing import Dict, List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session

from app import deps
from app.db.session import get_db
from app.services.financial_data import FinancialDataService
from app.services.technical_analysis import TechnicalAnalysisService

router = APIRouter()


@router.get("/asset/{symbol}")
async def get_asset_data(
    symbol: str,
    period: str = Query(
        "1y",
        description=(
            "Période de données (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"
        ),
    ),
    interval: str = Query(
        "1d",
        description=(
            "Intervalle de temps (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)"
        ),
    ),
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Dict[str, object]:
    """Récupérer les données historiques d'un actif financier."""
    _ = db, current_user  # Les paramètres sont utilisés par la dépendance pour la sécurité
    financial_service = FinancialDataService()
    return await financial_service.get_asset_data(symbol, period, interval)


@router.get("/search")
async def search_assets(
    query: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> List[Dict[str, object]]:
    """Rechercher des actifs financiers par nom ou symbole."""
    _ = db, current_user
    financial_service = FinancialDataService()
    return await financial_service.search_assets(query)


@router.post("/technical-indicators")
async def calculate_technical_indicators(
    symbol: str,
    indicators: List[str] | None = Query(
        None, description="Liste des indicateurs à calculer"
    ),
    period: str = Query("1y", description="Période de données"),
    interval: str = Query("1d", description="Intervalle de temps"),
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Dict[str, object]:
    """Calculer les indicateurs techniques pour un actif financier."""
    _ = db, current_user
    financial_service = FinancialDataService()
    asset_data = await financial_service.get_asset_data(symbol, period, interval)

    if "error" in asset_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Données non disponibles pour {symbol}",
        )

    df = pd.DataFrame(asset_data["historical_data"])
    ta_service = TechnicalAnalysisService()
    result_df = ta_service.calculate_indicators(df, indicators)

    return {
        "symbol": symbol,
        "indicators": indicators or [],
        "data": result_df.to_dict(orient="records"),
    }


@router.post("/ict-analysis")
async def calculate_ict_concepts(
    symbol: str,
    concepts: List[str] | None = Query(
        None, description="Liste des concepts ICT à calculer"
    ),
    period: str = Query("1y", description="Période de données"),
    interval: str = Query("1d", description="Intervalle de temps"),
    db: Session = Depends(get_db),
    current_user: Dict[str, int] = Depends(deps.get_current_user),
) -> Dict[str, object]:
    """Calculer les concepts ICT (Smart Money Concept) pour un actif financier."""
    _ = db, current_user
    financial_service = FinancialDataService()
    asset_data = await financial_service.get_asset_data(symbol, period, interval)

    if "error" in asset_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Données non disponibles pour {symbol}",
        )

    df = pd.DataFrame(asset_data["historical_data"])

    ta_service = TechnicalAnalysisService()
    df = ta_service.calculate_indicators(df, ["atr"])
    ict_results = ta_service.calculate_ict_concepts(df, concepts)

    return {
        "symbol": symbol,
        "concepts": concepts or [],
        "data": ict_results,
    }
