from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_portfolios():
    return {"message": "Liste des portfolios"}