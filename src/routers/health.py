from fastapi import APIRouter

router = APIRouter(prefix="/health", tags=["Salud"])


@router.get("/")
def health_check():
    return {"status": "ok", "message": "API operativa"}
