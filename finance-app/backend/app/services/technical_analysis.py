import pandas as pd
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime


def _format_index(index_value: Any) -> str:
    """Formatte l'index d'une série pandas pour l'inclure dans la réponse JSON."""

    if isinstance(index_value, datetime):
        return index_value.strftime("%Y-%m-%d")
    return str(index_value)

class TechnicalAnalysisService:
    """
    Service pour calculer les indicateurs techniques classiques et les concepts ICT.
    """
    
    @staticmethod
    def calculate_indicators(data: pd.DataFrame, indicators: List[str] = None) -> pd.DataFrame:
        """
        Calcule les indicateurs techniques demandés sur les données fournies.
        
        Args:
            data: DataFrame avec les colonnes OHLCV (Open, High, Low, Close, Volume)
            indicators: Liste des indicateurs à calculer (par défaut, tous les indicateurs)
            
        Returns:
            DataFrame avec les indicateurs ajoutés
        """
        # Copie des données pour éviter de modifier l'original
        df = data.copy()
        
        # Liste des indicateurs disponibles
        available_indicators = [
            "sma", "ema", "rsi", "macd", "bollinger_bands", 
            "stochastic", "atr", "adx", "obv", "trix"
        ]
        
        # Si aucun indicateur n'est spécifié, calculer tous les indicateurs
        indicators = indicators or available_indicators
        
        # Calcul des indicateurs demandés
        for indicator in indicators:
            if indicator == "sma":
                df = TechnicalAnalysisService._add_sma(df)
            elif indicator == "ema":
                df = TechnicalAnalysisService._add_ema(df)
            elif indicator == "rsi":
                df = TechnicalAnalysisService._add_rsi(df)
            elif indicator == "macd":
                df = TechnicalAnalysisService._add_macd(df)
            elif indicator == "bollinger_bands":
                df = TechnicalAnalysisService._add_bollinger_bands(df)
            elif indicator == "stochastic":
                df = TechnicalAnalysisService._add_stochastic(df)
            elif indicator == "atr":
                df = TechnicalAnalysisService._add_atr(df)
            elif indicator == "adx":
                df = TechnicalAnalysisService._add_adx(df)
            elif indicator == "obv":
                df = TechnicalAnalysisService._add_obv(df)
            elif indicator == "trix":
                df = TechnicalAnalysisService._add_trix(df)
        
        return df
    
    @staticmethod
    def calculate_ict_concepts(data: pd.DataFrame, concepts: List[str] = None) -> Dict[str, Any]:
        """
        Calcule les concepts ICT (Smart Money Concept) sur les données fournies.
        
        Args:
            data: DataFrame avec les colonnes OHLCV (Open, High, Low, Close, Volume)
            concepts: Liste des concepts ICT à calculer (par défaut, tous les concepts)
            
        Returns:
            Dictionnaire avec les concepts ICT calculés
        """
        # Copie des données pour éviter de modifier l'original
        df = data.copy()
        
        # Liste des concepts ICT disponibles
        available_concepts = [
            "fair_value_gap", "order_blocks", "liquidity", 
            "equal_highs_lows", "breaker_blocks", "imbalance"
        ]
        
        # Si aucun concept n'est spécifié, calculer tous les concepts
        concepts = concepts or available_concepts
        
        # Dictionnaire pour stocker les résultats
        ict_results = {}
        
        # Calcul des concepts ICT demandés
        for concept in concepts:
            if concept == "fair_value_gap":
                ict_results["fair_value_gap"] = TechnicalAnalysisService._find_fair_value_gaps(df)
            elif concept == "order_blocks":
                ict_results["order_blocks"] = TechnicalAnalysisService._find_order_blocks(df)
            elif concept == "liquidity":
                ict_results["liquidity"] = TechnicalAnalysisService._find_liquidity_levels(df)
            elif concept == "equal_highs_lows":
                ict_results["equal_highs_lows"] = TechnicalAnalysisService._find_equal_highs_lows(df)
            elif concept == "breaker_blocks":
                ict_results["breaker_blocks"] = TechnicalAnalysisService._find_breaker_blocks(df)
            elif concept == "imbalance":
                ict_results["imbalance"] = TechnicalAnalysisService._find_imbalance(df)
        
        return ict_results
    
    # Méthodes pour les indicateurs techniques classiques
    
    @staticmethod
    def _add_sma(df: pd.DataFrame, periods: List[int] = [20, 50, 200]) -> pd.DataFrame:
        """Ajoute les moyennes mobiles simples (SMA)"""
        for period in periods:
            df[f'SMA_{period}'] = df['Close'].rolling(window=period).mean()
        return df
    
    @staticmethod
    def _add_ema(df: pd.DataFrame, periods: List[int] = [9, 21, 55, 200]) -> pd.DataFrame:
        """Ajoute les moyennes mobiles exponentielles (EMA)"""
        for period in periods:
            df[f'EMA_{period}'] = df['Close'].ewm(span=period, adjust=False).mean()
        return df
    
    @staticmethod
    def _add_rsi(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Ajoute l'indicateur de force relative (RSI)"""
        delta = df['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()
        
        rs = avg_gain / avg_loss
        df['RSI'] = 100 - (100 / (1 + rs))
        return df
    
    @staticmethod
    def _add_macd(df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> pd.DataFrame:
        """Ajoute l'indicateur MACD (Moving Average Convergence Divergence)"""
        ema_fast = df['Close'].ewm(span=fast, adjust=False).mean()
        ema_slow = df['Close'].ewm(span=slow, adjust=False).mean()
        
        df['MACD'] = ema_fast - ema_slow
        df['MACD_Signal'] = df['MACD'].ewm(span=signal, adjust=False).mean()
        df['MACD_Histogram'] = df['MACD'] - df['MACD_Signal']
        return df
    
    @staticmethod
    def _add_bollinger_bands(df: pd.DataFrame, period: int = 20, std_dev: int = 2) -> pd.DataFrame:
        """Ajoute les bandes de Bollinger"""
        df['BB_Middle'] = df['Close'].rolling(window=period).mean()
        df['BB_Std'] = df['Close'].rolling(window=period).std()
        
        df['BB_Upper'] = df['BB_Middle'] + (df['BB_Std'] * std_dev)
        df['BB_Lower'] = df['BB_Middle'] - (df['BB_Std'] * std_dev)
        return df
    
    @staticmethod
    def _add_stochastic(df: pd.DataFrame, k_period: int = 14, d_period: int = 3) -> pd.DataFrame:
        """Ajoute l'oscillateur stochastique"""
        low_min = df['Low'].rolling(window=k_period).min()
        high_max = df['High'].rolling(window=k_period).max()
        
        df['Stoch_K'] = 100 * ((df['Close'] - low_min) / (high_max - low_min))
        df['Stoch_D'] = df['Stoch_K'].rolling(window=d_period).mean()
        return df
    
    @staticmethod
    def _add_atr(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Ajoute l'Average True Range (ATR)"""
        high_low = df['High'] - df['Low']
        high_close = (df['High'] - df['Close'].shift()).abs()
        low_close = (df['Low'] - df['Close'].shift()).abs()
        
        ranges = pd.concat([high_low, high_close, low_close], axis=1)
        true_range = ranges.max(axis=1)
        
        df['ATR'] = true_range.rolling(window=period).mean()
        return df
    
    @staticmethod
    def _add_adx(df: pd.DataFrame, period: int = 14) -> pd.DataFrame:
        """Ajoute l'Average Directional Index (ADX)"""
        # Calcul de l'ATR
        df = TechnicalAnalysisService._add_atr(df, period)
        
        # Calcul des Directional Movements
        df['UpMove'] = df['High'] - df['High'].shift(1)
        df['DownMove'] = df['Low'].shift(1) - df['Low']
        
        df['PlusDM'] = np.where((df['UpMove'] > df['DownMove']) & (df['UpMove'] > 0), df['UpMove'], 0)
        df['MinusDM'] = np.where((df['DownMove'] > df['UpMove']) & (df['DownMove'] > 0), df['DownMove'], 0)
        
        # Calcul des Directional Indicators
        df['PlusDI'] = 100 * (df['PlusDM'].rolling(window=period).mean() / df['ATR'])
        df['MinusDI'] = 100 * (df['MinusDM'].rolling(window=period).mean() / df['ATR'])
        
        # Calcul de l'ADX
        df['DX'] = 100 * (abs(df['PlusDI'] - df['MinusDI']) / (df['PlusDI'] + df['MinusDI']))
        df['ADX'] = df['DX'].rolling(window=period).mean()
        
        return df
    
    @staticmethod
    def _add_obv(df: pd.DataFrame) -> pd.DataFrame:
        """Ajoute l'On-Balance Volume (OBV)"""
        df['OBV'] = np.where(df['Close'] > df['Close'].shift(1), 
                             df['Volume'], 
                             np.where(df['Close'] < df['Close'].shift(1), 
                                     -df['Volume'], 0)).cumsum()
        return df
    
    @staticmethod
    def _add_trix(df: pd.DataFrame, period: int = 15) -> pd.DataFrame:
        """Ajoute l'indicateur TRIX"""
        ema1 = df['Close'].ewm(span=period, adjust=False).mean()
        ema2 = ema1.ewm(span=period, adjust=False).mean()
        ema3 = ema2.ewm(span=period, adjust=False).mean()
        
        df['TRIX'] = 100 * (ema3 - ema3.shift(1)) / ema3.shift(1)
        return df
    
    # Méthodes pour les concepts ICT (Smart Money Concept)
    
    @staticmethod
    def _find_fair_value_gaps(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """
        Identifie les Fair Value Gaps (FVG) dans les données.
        Un FVG se produit lorsqu'il y a un écart entre les bougies, généralement après une forte impulsion.
        """
        fvgs = []
        
        # Parcourir les données pour trouver les FVG
        for i in range(2, len(df)):
            # FVG haussier: Low[i] > High[i-2]
            if df['Low'].iloc[i] > df['High'].iloc[i-2]:
                fvgs.append({
                    'type': 'bullish',
                    'date': df.index[i].strftime('%Y-%m-%d') if isinstance(df.index[i], datetime) else str(df.index[i]),
                    'level_top': float(df['Low'].iloc[i]),
                    'level_bottom': float(df['High'].iloc[i-2]),
                    'size': float(df['Low'].iloc[i] - df['High'].iloc[i-2])
                })
            
            # FVG baissier: High[i] < Low[i-2]
            elif df['High'].iloc[i] < df['Low'].iloc[i-2]:
                fvgs.append({
                    'type': 'bearish',
                    'date': df.index[i].strftime('%Y-%m-%d') if isinstance(df.index[i], datetime) else str(df.index[i]),
                    'level_top': float(df['Low'].iloc[i-2]),
                    'level_bottom': float(df['High'].iloc[i]),
                    'size': float(df['Low'].iloc[i-2] - df['High'].iloc[i])
                })
        
        return fvgs
    
    @staticmethod
    def _find_order_blocks(df: pd.DataFrame, lookback: int = 10) -> List[Dict[str, Any]]:
        """
        Identifie les Order Blocks dans les données.
        Un Order Block est une bougie qui précède une forte impulsion dans la direction opposée.
        """
        order_blocks = []
        
        # Parcourir les données pour trouver les Order Blocks
        for i in range(lookback, len(df)-1):
            # Calculer le mouvement après la bougie actuelle
            next_move = df['Close'].iloc[i+1] - df['Open'].iloc[i+1]
            
            # Order Block haussier (bougie baissière suivie d'une forte hausse)
            if next_move > 0 and abs(next_move) > df['ATR'].iloc[i] * 1.5 and df['Close'].iloc[i] < df['Open'].iloc[i]:
                order_blocks.append({
                    'type': 'bullish',
                    'date': df.index[i].strftime('%Y-%m-%d') if isinstance(df.index[i], datetime) else str(df.index[i]),
                    'level_top': float(df['Open'].iloc[i]),
                    'level_bottom': float(df['Close'].iloc[i]),
                    'strength': float(abs(next_move) / df['ATR'].iloc[i])
                })
            
            # Order Block baissier (bougie haussière suivie d'une forte baisse)
            elif next_move < 0 and abs(next_move) > df['ATR'].iloc[i] * 1.5 and df['Close'].iloc[i] > df['Open'].iloc[i]:
                order_blocks.append({
                    'type': 'bearish',
                    'date': df.index[i].strftime('%Y-%m-%d') if isinstance(df.index[i], datetime) else str(df.index[i]),
                    'level_top': float(df['Close'].iloc[i]),
                    'level_bottom': float(df['Open'].iloc[i]),
                    'strength': float(abs(next_move) / df['ATR'].iloc[i])
                })
        
        return order_blocks
    
    @staticmethod
    def _find_liquidity_levels(df: pd.DataFrame, window: int = 5) -> List[Dict[str, Any]]:
        """
        Identifie les niveaux de liquidité dans les données.
        Les niveaux de liquidité sont des zones où il y a une accumulation de stops (swing highs/lows).
        """
        liquidity_levels = []
        
        # Trouver les swing highs et lows
        for i in range(window, len(df)-window):
            # Vérifier si c'est un swing high
            is_swing_high = True
            for j in range(1, window+1):
                if df['High'].iloc[i] <= df['High'].iloc[i-j] or df['High'].iloc[i] <= df['High'].iloc[i+j]:
                    is_swing_high = False
                    break
            
            if is_swing_high:
                liquidity_levels.append({
                    'type': 'high',
                    'date': df.index[i].strftime('%Y-%m-%d') if isinstance(df.index[i], datetime) else str(df.index[i]),
                    'level': float(df['High'].iloc[i]),
                    'volume': float(df['Volume'].iloc[i])
                })
            
            # Vérifier si c'est un swing low
            is_swing_low = True
            for j in range(1, window+1):
                if df['Low'].iloc[i] >= df['Low'].iloc[i-j] or df['Low'].iloc[i] >= df['Low'].iloc[i+j]:
                    is_swing_low = False
                    break
            
            if is_swing_low:
                liquidity_levels.append({
                    'type': 'low',
                    'date': df.index[i].strftime('%Y-%m-%d') if isinstance(df.index[i], datetime) else str(df.index[i]),
                    'level': float(df['Low'].iloc[i]),
                    'volume': float(df['Volume'].iloc[i])
                })
        
        return liquidity_levels
    
    @staticmethod
    def _find_equal_highs_lows(
        df: pd.DataFrame, tolerance: float = 0.001
    ) -> List[Dict[str, Any]]:
        """Identifie les Equal Highs et Equal Lows dans les données de marché."""

        equal_levels: List[Dict[str, Any]] = []
        if df.empty:
            return equal_levels

        tolerance_value = (
            df["ATR"].mean() * tolerance
            if "ATR" in df.columns and not df["ATR"].isna().all()
            else df["Close"].mean() * tolerance
        )

        lookback = 20
        for i in range(1, len(df)):
            for j in range(max(0, i - lookback), i):
                if abs(df["High"].iloc[i] - df["High"].iloc[j]) <= tolerance_value:
                    equal_levels.append(
                        {
                            "type": "equal_high",
                            "date1": _format_index(df.index[j]),
                            "date2": _format_index(df.index[i]),
                            "level": float(df["High"].iloc[i]),
                            "difference": float(
                                abs(df["High"].iloc[i] - df["High"].iloc[j])
                            ),
                        }
                    )
                    break

        for i in range(1, len(df)):
            for j in range(max(0, i - lookback), i):
                if abs(df["Low"].iloc[i] - df["Low"].iloc[j]) <= tolerance_value:
                    equal_levels.append(
                        {
                            "type": "equal_low",
                            "date1": _format_index(df.index[j]),
                            "date2": _format_index(df.index[i]),
                            "level": float(df["Low"].iloc[i]),
                            "difference": float(
                                abs(df["Low"].iloc[i] - df["Low"].iloc[j])
                            ),
                        }
                    )
                    break

        return equal_levels

    @staticmethod
    def _find_breaker_blocks(df: pd.DataFrame, lookback: int = 5) -> List[Dict[str, Any]]:
        """Détecte des breaker blocks simples à partir des cassures de structure."""

        breaker_blocks: List[Dict[str, Any]] = []
        if len(df) <= lookback:
            return breaker_blocks

        for i in range(lookback, len(df)):
            previous_high = float(df["High"].iloc[i - lookback : i].max())
            previous_low = float(df["Low"].iloc[i - lookback : i].min())
            close_price = float(df["Close"].iloc[i])
            date = _format_index(df.index[i])

            if close_price > previous_high:
                breaker_blocks.append(
                    {
                        "type": "bullish",
                        "date": date,
                        "level": previous_high,
                        "confirmation": close_price,
                    }
                )
            elif close_price < previous_low:
                breaker_blocks.append(
                    {
                        "type": "bearish",
                        "date": date,
                        "level": previous_low,
                        "confirmation": close_price,
                    }
                )

        return breaker_blocks

    @staticmethod
    def _find_imbalance(df: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identifie les zones d'imbalance (gaps) entre deux bougies consécutives."""

        imbalances: List[Dict[str, Any]] = []
        for i in range(1, len(df)):
            current_low = float(df["Low"].iloc[i])
            current_high = float(df["High"].iloc[i])
            previous_high = float(df["High"].iloc[i - 1])
            previous_low = float(df["Low"].iloc[i - 1])

            if current_low > previous_high:
                imbalances.append(
                    {
                        "type": "gap_up",
                        "date": _format_index(df.index[i]),
                        "upper": current_low,
                        "lower": previous_high,
                    }
                )
            elif current_high < previous_low:
                imbalances.append(
                    {
                        "type": "gap_down",
                        "date": _format_index(df.index[i]),
                        "upper": previous_low,
                        "lower": current_high,
                    }
                )

        return imbalances
