from fastapi import APIRouter, Depends
from middleware_client import get_current_user

router = APIRouter(prefix="/protected", tags=["protected"])

@router.get("/profile")
def profile(user = Depends(get_current_user)):
    return {
        "id": user.id,
        "email": user.email,
        "created_at": user.created_at
    }

@router.get("/dashboard")
def dashboard(user = Depends(get_current_user)):
    return { "message": f"Welcome, {user.email}" }

