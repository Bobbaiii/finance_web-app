from fastapi import APIRouter
from .users import router as users_router
from .portfolios import router as portfolios_router
from .alerts import router as alerts_router
from .analysis import router as analysis_router

api_router = APIRouter()
api_router.include_router(users_router, prefix="/users", tags=["users"])
api_router.include_router(portfolios_router, prefix="/portfolios", tags=["portfolios"])
api_router.include_router(alerts_router, prefix="/alerts", tags=["alerts"])
api_router.include_router(analysis_router, prefix="/analysis", tags=["analysis"])
