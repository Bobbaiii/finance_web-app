from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_alerts():
    return {"message": "Liste des alertes"}
