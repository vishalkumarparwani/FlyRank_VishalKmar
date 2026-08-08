from fastapi import APIRouter, HTTPException, Depends
from supabase_client import supabase
from pydantic import BaseModel, EmailStr
from middleware_client import get_current_user

router = APIRouter(prefix="/auth", tags=["authentication"])

class AuthRequest(BaseModel):
    email: EmailStr
    password: str

@router.post("/signup", status_code=201)
def signup(user: AuthRequest):
    if not user.email or not user.password:
        raise HTTPException(
            status_code=400,
            detail="Email and password required"
        )

    if len(user.password) < 6:
         raise HTTPException(
            status_code=400,
            detail="Password must be at least 6 characters"
    )

    response = supabase.auth.sign_up(
        {
            "email": user.email,
            "password": user.password
        }
    )

    if response.user is None:
        raise HTTPException(
            status_code=400,
            detail="Signup failed"
        )

    return { "user": response.user }


@router.post("/login")
def login(user: AuthRequest):
    if not user.email or not user.password:
            raise HTTPException(
                status_code=400,
                detail="Email and password required"
            )

    response = supabase.auth.sign_in_with_password(
            {
                "email": user.email,
                "password": user.password
            }
        )
    
    if response.user is None:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )

    return {
        "access_token": response.session.access_token,
        "refresh_token": response.session.refresh_token,
        "expires_at": response.session.expires_at,
        "user": response.user
    }


@router.post("/logout", status_code=204)
def logout(token: str, user = Depends(get_current_user)):
    supabase.auth.sign_out()
    return
