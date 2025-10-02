import yfinance as yf
from typing import List, Dict, Any, Optional
from app.core.config import settings

class FinancialDataService:
    """
    Service pour récupérer et traiter les données financières depuis différentes API.
    Supporte actuellement yfinance, avec possibilité d'extension à d'autres API.
    """
    
    def __init__(self, api_source: str = None):
        self.api_source = api_source or settings.DEFAULT_FINANCIAL_API
    
    async def get_asset_data(
        self, 
        symbol: str, 
        period: str = "1y", 
        interval: str = "1d"
    ) -> Dict[str, Any]:
        """
        Récupère les données historiques d'un actif financier.
        
        Args:
            symbol: Symbole de l'actif (ex: AAPL, BTC-USD)
            period: Période de données (1d, 5d, 1mo, 3mo, 6mo, 1y, 2y, 5y, 10y, ytd, max)
            interval: Intervalle de temps (1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo)
            
        Returns:
            Dictionnaire contenant les informations de l'actif et les données historiques
        """
        if self.api_source == "yfinance":
            return await self._get_data_from_yfinance(symbol, period, interval)
        else:
            raise ValueError(f"Source API non supportée: {self.api_source}")
    
    async def _get_data_from_yfinance(
        self, 
        symbol: str, 
        period: str, 
        interval: str
    ) -> Dict[str, Any]:
        """Récupère les données depuis Yahoo Finance"""
        try:
            # Récupération des informations de l'actif
            ticker = yf.Ticker(symbol)
            info = ticker.info
            
            # Récupération des données historiques
            hist = ticker.history(period=period, interval=interval)
            
            # Conversion en format compatible avec JSON
            hist_dict = hist.reset_index().to_dict(orient="records")
            
            # Extraction des informations pertinentes
            asset_info = {
                "symbol": symbol,
                "name": info.get("shortName", ""),
                "sector": info.get("sector", ""),
                "industry": info.get("industry", ""),
                "currency": info.get("currency", ""),
                "exchange": info.get("exchange", ""),
                "market_cap": info.get("marketCap", None),
                "current_price": info.get("currentPrice", None),
                "fifty_two_week_high": info.get("fiftyTwoWeekHigh", None),
                "fifty_two_week_low": info.get("fiftyTwoWeekLow", None),
                "average_volume": info.get("averageVolume", None),
                "pe_ratio": info.get("trailingPE", None),
                "dividend_yield": info.get("dividendYield", None) * 100 if info.get("dividendYield") else None,
            }
            
            return {
                "asset_info": asset_info,
                "historical_data": hist_dict
            }
            
        except Exception as e:
            return {
                "error": str(e),
                "asset_info": {"symbol": symbol},
                "historical_data": []
            }
    
    async def search_assets(self, query: str) -> List[Dict[str, Any]]:
        """
        Recherche des actifs financiers par nom ou symbole.
        
        Args:
            query: Terme de recherche
            
        Returns:
            Liste des actifs correspondants
        """
        # Cette fonction est simplifiée et pourrait être améliorée avec une API dédiée
        try:
            tickers = yf.Tickers(query)
            results = []
            
            for symbol in query.split():
                try:
                    ticker = tickers.tickers.get(symbol)
                    if ticker:
                        info = ticker.info
                        results.append({
                            "symbol": symbol,
                            "name": info.get("shortName", ""),
                            "type": self._determine_asset_type(symbol, info),
                            "exchange": info.get("exchange", ""),
                            "currency": info.get("currency", "")
                        })
                except:
                    pass
                    
            return results
        except Exception as e:
            return [{"error": str(e)}]
    
    def _determine_asset_type(self, symbol: str, info: Dict[str, Any]) -> str:
        """Détermine le type d'actif en fonction du symbole et des informations"""
        if "-USD" in symbol:
            return "crypto"
        elif "=" in symbol:
            return "forex"
        elif symbol.startswith("^"):
            return "index"
        elif info.get("quoteType") == "CRYPTOCURRENCY":
            return "crypto"
        elif info.get("quoteType") == "INDEX":
            return "index"
        elif info.get("quoteType") == "CURRENCY":
            return "forex"
        elif info.get("sector") in ["Basic Materials", "Energy"]:
            return "commodity"
        else:
            return "stock"
