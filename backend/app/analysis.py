from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Dict, Any, Optional
from app.db.session import get_db
from app.services.financial_data import FinancialDataService
from app.services.technical_analysis import TechnicalAnalysisService
from app.api.deps import get_current_user
import pandas as pd

router = APIRouter()

@router.get("/asset/{symbol}")
async def get_asset_data(
    symbol: str,
    period: str = Query("1y", description="Période de données (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)"),
    interval: str = Query("1d", description="Intervalle de temps (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Récupère les données historiques d'un actif financier.
    """
    financial_service = FinancialDataService()
    return await financial_service.get_asset_data(symbol, period, interval)

@router.get("/search")
async def search_assets(
    query: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Recherche des actifs financiers par nom ou symbole.
    """
    financial_service = FinancialDataService()
    return await financial_service.search_assets(query)

@router.post("/technical-indicators")
async def calculate_technical_indicators(
    symbol: str,
    indicators: List[str] = Query(None, description="Liste des indicateurs à calculer"),
    period: str = Query("1y", description="Période de données"),
    interval: str = Query("1d", description="Intervalle de temps"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Calcule les indicateurs techniques pour un actif financier.
    """
    # Récupérer les données de l'actif
    financial_service = FinancialDataService()
    asset_data = await financial_service.get_asset_data(symbol, period, interval)
    
    if "error" in asset_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Données non disponibles pour {symbol}"
        )
    
    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(asset_data["historical_data"])
    
    # Calculer les indicateurs techniques
    ta_service = TechnicalAnalysisService()
    result_df = ta_service.calculate_indicators(df, indicators)
    
    # Convertir le DataFrame en dictionnaire pour la réponse JSON
    result_dict = result_df.to_dict(orient="records")
    
    return {
        "symbol": symbol,
        "indicators": indicators,
        "data": result_dict
    }

@router.post("/ict-analysis")
async def calculate_ict_concepts(
    symbol: str,
    concepts: List[str] = Query(None, description="Liste des concepts ICT à calculer"),
    period: str = Query("1y", description="Période de données"),
    interval: str = Query("1d", description="Intervalle de temps"),
    db: Session = Depends(get_db),
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Calcule les concepts ICT (Smart Money Concept) pour un actif financier.
    """
    # Récupérer les données de l'actif
    financial_service = FinancialDataService()
    asset_data = await financial_service.get_asset_data(symbol, period, interval)
    
    if "error" in asset_data:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Données non disponibles pour {symbol}"
        )
    
    # Convertir les données en DataFrame pandas
    df = pd.DataFrame(asset_data["historical_data"])
    
    # Calculer les indicateurs techniques nécessaires pour l'analyse ICT
    ta_service = TechnicalAnalysisService()
    df = ta_service.calculate_indicators(df, ["atr"])
    
    # Calculer les concepts ICT
    ict_results = ta_service.calculate_ict_concepts(df, concepts)
    
    return {
        "symbol": symbol,
        "concepts": concepts,
        "data": ict_results
    }
