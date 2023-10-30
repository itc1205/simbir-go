from fastapi import APIRouter

router = APIRouter(
    prefix="/Admin",
    tags=["Admin"]
)

@router.get("/ping")
def ping_admin():
    return "pong!"