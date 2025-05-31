from fastapi import APIRouter
from app.api.routes import users, portfolios, alerts, analysis

api_router = APIRouter()

# Inclure les routes pour chaque module
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
