from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base_class import Base
from uuid import uuid4

# Table d'association pour les actifs favoris
favorite_assets = Table(
    "favorite_assets",
    Base.metadata,
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True),
    Column("asset_id", Integer, ForeignKey("assets.id"), primary_key=True),
)

# Table d'association pour les actifs en portefeuille
portfolio_assets = Table(
    "portfolio_assets",
    Base.metadata,
    Column("portfolio_id", Integer, ForeignKey("portfolios.id"), primary_key=True),
    Column("asset_id", Integer, ForeignKey("assets.id"), primary_key=True),
    Column("quantity", Float, default=0),
    Column("entry_price", Float),
    Column("entry_date", DateTime, default=func.now()),
)

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, index=True)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relations
    portfolios = relationship("Portfolio", back_populates="owner")
    alerts = relationship("Alert", back_populates="user")
    favorite_assets = relationship("Asset", secondary=favorite_assets, back_populates="favorited_by")
    notification_settings = relationship("NotificationSetting", back_populates="user", uselist=False)

class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, index=True)
    asset_type = Column(String, index=True)  # stock, index, crypto, forex, commodity
    exchange = Column(String, index=True)
    currency = Column(String)
    last_price = Column(Float)
    last_updated = Column(DateTime)
    
    # Relations
    favorited_by = relationship("User", secondary=favorite_assets, back_populates="favorite_assets")
    portfolios = relationship("Portfolio", secondary=portfolio_assets, back_populates="assets")
    alerts = relationship("Alert", back_populates="asset")
    
class Portfolio(Base):
    __tablename__ = "portfolios"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    
    # Relations
    owner = relationship("User", back_populates="portfolios")
    assets = relationship("Asset", secondary=portfolio_assets, back_populates="portfolios")
    transactions = relationship("Transaction", back_populates="portfolio")

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    portfolio_id = Column(Integer, ForeignKey("portfolios.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    transaction_type = Column(String)  # buy, sell
    quantity = Column(Float)
    price = Column(Float)
    total_value = Column(Float)
    transaction_date = Column(DateTime, default=func.now())
    notes = Column(String)
    
    # Relations
    portfolio = relationship("Portfolio", back_populates="transactions")
    asset = relationship("Asset")

class Alert(Base):
    __tablename__ = "alerts"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    asset_id = Column(Integer, ForeignKey("assets.id"))
    alert_type = Column(String)  # price, ict_zone, indicator
    condition = Column(String)  # above, below, crosses
    value = Column(Float)
    is_active = Column(Boolean, default=True)
    is_repeatable = Column(Boolean, default=False)
    created_at = Column(DateTime, default=func.now())
    last_triggered = Column(DateTime)
    
    # Relations
    user = relationship("User", back_populates="alerts")
    asset = relationship("Asset", back_populates="alerts")
    
class NotificationSetting(Base):
    __tablename__ = "notification_settings"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    email_enabled = Column(Boolean, default=True)
    telegram_enabled = Column(Boolean, default=False)
    telegram_chat_id = Column(String)
    whatsapp_enabled = Column(Boolean, default=False)
    whatsapp_number = Column(String)
    
    # Relations
    user = relationship("User", back_populates="notification_settings")
