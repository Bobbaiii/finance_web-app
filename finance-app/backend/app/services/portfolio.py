from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session

from app.models import Portfolio, Asset, Transaction, User
from app.schemas import PortfolioCreate, PortfolioUpdate, TransactionCreate
from datetime import datetime

class PortfolioService:
    """
    Service pour la gestion des portefeuilles et des transactions.
    """
    
    @staticmethod
    async def create_portfolio(db: Session, portfolio: PortfolioCreate, user_id: int) -> Portfolio:
        """
        Crée un nouveau portefeuille pour un utilisateur.
        
        Args:
            db: Session de base de données
            portfolio: Données du portefeuille à créer
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            Le portefeuille créé
        """
        db_portfolio = Portfolio(
            name=portfolio.name,
            description=portfolio.description,
            owner_id=user_id
        )
        db.add(db_portfolio)
        db.commit()
        db.refresh(db_portfolio)
        return db_portfolio
    
    @staticmethod
    async def get_portfolios(db: Session, user_id: int) -> List[Portfolio]:
        """
        Récupère tous les portefeuilles d'un utilisateur.
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            
        Returns:
            Liste des portefeuilles de l'utilisateur
        """
        return db.query(Portfolio).filter(Portfolio.owner_id == user_id).all()
    
    @staticmethod
    async def get_portfolio(db: Session, portfolio_id: int, user_id: int) -> Optional[Portfolio]:
        """
        Récupère un portefeuille spécifique d'un utilisateur.
        
        Args:
            db: Session de base de données
            portfolio_id: ID du portefeuille
            user_id: ID de l'utilisateur
            
        Returns:
            Le portefeuille s'il existe et appartient à l'utilisateur, None sinon
        """
        return db.query(Portfolio).filter(
            Portfolio.id == portfolio_id,
            Portfolio.owner_id == user_id
        ).first()
    
    @staticmethod
    async def update_portfolio(
        db: Session, 
        portfolio_id: int, 
        portfolio_update: PortfolioUpdate, 
        user_id: int
    ) -> Optional[Portfolio]:
        """
        Met à jour un portefeuille existant.
        
        Args:
            db: Session de base de données
            portfolio_id: ID du portefeuille à mettre à jour
            portfolio_update: Données de mise à jour
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            Le portefeuille mis à jour s'il existe et appartient à l'utilisateur, None sinon
        """
        db_portfolio = await PortfolioService.get_portfolio(db, portfolio_id, user_id)
        if not db_portfolio:
            return None
        
        update_data = portfolio_update.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_portfolio, key, value)
        
        db_portfolio.updated_at = datetime.now()
        db.commit()
        db.refresh(db_portfolio)
        return db_portfolio
    
    @staticmethod
    async def delete_portfolio(db: Session, portfolio_id: int, user_id: int) -> bool:
        """
        Supprime un portefeuille.
        
        Args:
            db: Session de base de données
            portfolio_id: ID du portefeuille à supprimer
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            True si le portefeuille a été supprimé, False sinon
        """
        db_portfolio = await PortfolioService.get_portfolio(db, portfolio_id, user_id)
        if not db_portfolio:
            return False
        
        db.delete(db_portfolio)
        db.commit()
        return True
    
    @staticmethod
    async def add_transaction(db: Session, transaction: TransactionCreate, user_id: int) -> Optional[Transaction]:
        """
        Ajoute une transaction à un portefeuille.
        
        Args:
            db: Session de base de données
            transaction: Données de la transaction
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            La transaction créée si le portefeuille existe et appartient à l'utilisateur, None sinon
        """
        # Vérifier que le portefeuille appartient à l'utilisateur
        db_portfolio = await PortfolioService.get_portfolio(db, transaction.portfolio_id, user_id)
        if not db_portfolio:
            return None
        
        # Vérifier que l'actif existe
        db_asset = db.query(Asset).filter(Asset.id == transaction.asset_id).first()
        if not db_asset:
            return None
        
        # Calculer la valeur totale si non fournie
        total_value = transaction.total_value
        if not total_value:
            total_value = transaction.quantity * transaction.price
        
        # Créer la transaction
        db_transaction = Transaction(
            portfolio_id=transaction.portfolio_id,
            asset_id=transaction.asset_id,
            transaction_type=transaction.transaction_type,
            quantity=transaction.quantity,
            price=transaction.price,
            total_value=total_value,
            transaction_date=transaction.transaction_date or datetime.now(),
            notes=transaction.notes
        )
        
        db.add(db_transaction)
        db.commit()
        db.refresh(db_transaction)
        
        # Mettre à jour la relation portfolio-asset
        # Si c'est un achat, ajouter l'actif au portefeuille ou mettre à jour la quantité
        if transaction.transaction_type.lower() == "buy":
            # Vérifier si l'actif est déjà dans le portefeuille
            portfolio_asset = db.query(Portfolio.assets).filter(
                Portfolio.id == transaction.portfolio_id,
                Asset.id == transaction.asset_id
            ).first()
            
            if not portfolio_asset:
                # Ajouter l'actif au portefeuille
                db_portfolio.assets.append(db_asset)
            else:
                # Mettre à jour la quantité
                for asset in db_portfolio.assets:
                    if asset.id == transaction.asset_id:
                        # La quantité est gérée dans la table d'association
                        pass
        
        db.commit()
        return db_transaction
    
    @staticmethod
    async def get_portfolio_performance(db: Session, portfolio_id: int, user_id: int) -> Dict[str, Any]:
        """
        Calcule les performances d'un portefeuille.
        
        Args:
            db: Session de base de données
            portfolio_id: ID du portefeuille
            user_id: ID de l'utilisateur propriétaire
            
        Returns:
            Dictionnaire contenant les métriques de performance du portefeuille
        """
        db_portfolio = await PortfolioService.get_portfolio(db, portfolio_id, user_id)
        if not db_portfolio:
            return {"error": "Portfolio not found"}
        
        # Récupérer toutes les transactions du portefeuille
        transactions = db.query(Transaction).filter(Transaction.portfolio_id == portfolio_id).all()
        
        # Calculer la valeur totale investie
        total_invested = 0
        current_value = 0
        holdings = {}
        
        for transaction in transactions:
            asset_id = transaction.asset_id
            
            # Initialiser l'actif dans les holdings s'il n'existe pas
            if asset_id not in holdings:
                holdings[asset_id] = {
                    "quantity": 0,
                    "total_cost": 0,
                    "current_value": 0,
                    "asset": transaction.asset
                }
            
            # Mettre à jour les holdings en fonction du type de transaction
            if transaction.transaction_type.lower() == "buy":
                holdings[asset_id]["quantity"] += transaction.quantity
                holdings[asset_id]["total_cost"] += transaction.total_value
                total_invested += transaction.total_value
            elif transaction.transaction_type.lower() == "sell":
                holdings[asset_id]["quantity"] -= transaction.quantity
                holdings[asset_id]["total_cost"] -= transaction.total_value
                total_invested -= transaction.total_value
        
        # Calculer la valeur actuelle du portefeuille
        for asset_id, holding in holdings.items():
            asset = holding["asset"]
            if asset.last_price:
                holding["current_value"] = holding["quantity"] * asset.last_price
                current_value += holding["current_value"]
        
        # Calculer les métriques de performance
        profit_loss = current_value - total_invested
        profit_loss_percentage = (profit_loss / total_invested * 100) if total_invested > 0 else 0
        
        return {
            "portfolio_id": portfolio_id,
            "portfolio_name": db_portfolio.name,
            "total_invested": total_invested,
            "current_value": current_value,
            "profit_loss": profit_loss,
            "profit_loss_percentage": profit_loss_percentage,
            "holdings": [
                {
                    "asset_id": asset_id,
                    "symbol": holding["asset"].symbol,
                    "name": holding["asset"].name,
                    "quantity": holding["quantity"],
                    "total_cost": holding["total_cost"],
                    "current_value": holding["current_value"],
                    "profit_loss": holding["current_value"] - holding["total_cost"],
                    "profit_loss_percentage": ((holding["current_value"] - holding["total_cost"]) / holding["total_cost"] * 100) if holding["total_cost"] > 0 else 0
                }
                for asset_id, holding in holdings.items()
                if holding["quantity"] > 0
            ]
        }
    
    @staticmethod
    async def add_asset_to_favorites(db: Session, asset_id: int, user_id: int) -> bool:
        """
        Ajoute un actif aux favoris d'un utilisateur.
        
        Args:
            db: Session de base de données
            asset_id: ID de l'actif à ajouter aux favoris
            user_id: ID de l'utilisateur
            
        Returns:
            True si l'actif a été ajouté aux favoris, False sinon
        """
        user = db.query(User).filter(User.id == user_id).first()
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        
        if not user or not asset:
            return False
        
        # Vérifier si l'actif est déjà dans les favoris
        if asset in user.favorite_assets:
            return True
        
        user.favorite_assets.append(asset)
        db.commit()
        return True
    
    @staticmethod
    async def remove_asset_from_favorites(db: Session, asset_id: int, user_id: int) -> bool:
        """
        Retire un actif des favoris d'un utilisateur.
        
        Args:
            db: Session de base de données
            asset_id: ID de l'actif à retirer des favoris
            user_id: ID de l'utilisateur
            
        Returns:
            True si l'actif a été retiré des favoris, False sinon
        """
        user = db.query(User).filter(User.id == user_id).first()
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        
        if not user or not asset:
            return False
        
        # Vérifier si l'actif est dans les favoris
        if asset not in user.favorite_assets:
            return True
        
        user.favorite_assets.remove(asset)
        db.commit()
        return True
    
    @staticmethod
    async def get_favorite_assets(db: Session, user_id: int) -> List[Asset]:
        """
        Récupère les actifs favoris d'un utilisateur.
        
        Args:
            db: Session de base de données
            user_id: ID de l'utilisateur
            
        Returns:
            Liste des actifs favoris de l'utilisateur
        """
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return []
        
        return user.favorite_assets
