from typing import List, Optional
from pydantic import BaseModel
from datetime import datetime

# Base Schemas
class AssetBase(BaseModel):
    symbol: str
    name: Optional[str] = None
    asset_type: str
    exchange: Optional[str] = None
    currency: Optional[str] = None

class PortfolioBase(BaseModel):
    name: str
    description: Optional[str] = None

class AlertBase(BaseModel):
    asset_id: int
    alert_type: str
    condition: str
    value: float
    is_active: bool = True
    is_repeatable: bool = False

# Create Schemas
class AssetCreate(AssetBase):
    pass

class PortfolioCreate(PortfolioBase):
    pass

class AlertCreate(AlertBase):
    pass

# Update Schemas
class AssetUpdate(BaseModel):
    name: Optional[str] = None
    last_price: Optional[float] = None
    last_updated: Optional[datetime] = None

class PortfolioUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None

class AlertUpdate(BaseModel):
    alert_type: Optional[str] = None
    condition: Optional[str] = None
    value: Optional[float] = None
    is_active: Optional[bool] = None
    is_repeatable: Optional[bool] = None

# Response Schemas
class Asset(AssetBase):
    id: int
    last_price: Optional[float] = None
    last_updated: Optional[datetime] = None

    class Config:
        orm_mode = True

class Portfolio(PortfolioBase):
    id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class PortfolioWithAssets(Portfolio):
    assets: List[Asset] = []

class Alert(AlertBase):
    id: int
    user_id: int
    created_at: datetime
    last_triggered: Optional[datetime] = None

    class Config:
        orm_mode = True

# Transaction Schemas
class TransactionBase(BaseModel):
    portfolio_id: int
    asset_id: int
    transaction_type: str
    quantity: float
    price: float
    total_value: Optional[float] = None
    notes: Optional[str] = None

class TransactionCreate(TransactionBase):
    transaction_date: Optional[datetime] = None

class Transaction(TransactionBase):
    id: int
    transaction_date: datetime
    asset: Asset

    class Config:
        orm_mode = True

# User Schemas
class UserBase(BaseModel):
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_superuser: bool = False
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True

class UserWithPortfolios(User):
    portfolios: List[Portfolio] = []

# Notification Settings Schemas
class NotificationSettingBase(BaseModel):
    email_enabled: bool = True
    telegram_enabled: bool = False
    telegram_chat_id: Optional[str] = None
    whatsapp_enabled: bool = False
    whatsapp_number: Optional[str] = None

class NotificationSettingCreate(NotificationSettingBase):
    user_id: int

class NotificationSetting(NotificationSettingBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class NotificationSettingUpdate(BaseModel):
    email_enabled: Optional[bool] = None
    telegram_enabled: Optional[bool] = None
    telegram_chat_id: Optional[str] = None
    whatsapp_enabled: Optional[bool] = None
    whatsapp_number: Optional[str] = None

# Token Schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenPayload(BaseModel):
    sub: Optional[int] = None
