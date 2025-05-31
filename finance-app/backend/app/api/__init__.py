# Version temporaire simplifiée pour démarrer l'application
from fastapi import FastAPI

app = FastAPI(title="Finance App API", description="API pour l'application Finance")

@app.get("/")
def read_root():
    return {"message": "Bienvenue sur l'API Finance App"}

# Décommentez progressivement les lignes ci-dessous une fois que les modules sont correctement configurés
# from fastapi import APIRouter
# api_router = APIRouter()
# from app.api.routes import users, portfolios, alerts, analysis
# api_router.include_router(users.router, prefix="/users", tags=["users"])
# api_router.include_router(portfolios.router, prefix="/portfolios", tags=["portfolios"])
# api_router.include_router(alerts.router, prefix="/alerts", tags=["alerts"])
# api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
# app.include_router(api_router)