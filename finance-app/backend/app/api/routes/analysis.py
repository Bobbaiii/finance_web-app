from fastapi import APIRouter

router = APIRouter()

@router.get("/")
def read_analysis():
    return {"message": "Analyse technique"}
