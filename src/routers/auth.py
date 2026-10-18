from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr
from typing import Dict
from src.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
import structlog

logger = structlog.get_logger()
router = APIRouter(prefix="/api/v1/auth", tags=["Authentication"])

FAKE_USERS_DB = {}

class UserRegisterRequest(BaseModel):
    email: EmailStr
    password: str
    role: str = "Recruiter"

class UserLoginRequest(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class RefreshTokenRequest(BaseModel):
    refresh_token: str

@router.post("/register", response_model=Dict[str, str], status_code=status.HTTP_201_CREATED)
async def register(payload: UserRegisterRequest):
    if payload.email in FAKE_USERS_DB:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_pwd = get_password_hash(payload.password)
    FAKE_USERS_DB[payload.email] = {
        "email": payload.email,
        "password": hashed_pwd,
        "role": payload.role
    }
    logger.info("user_registered", email=payload.email, role=payload.role)
    return {"message": "User registered successfully", "email": payload.email}

@router.post("/login", response_model=TokenResponse)
async def login(payload: UserLoginRequest):
    user = FAKE_USERS_DB.get(payload.email)
    if not user or not verify_password(payload.password, user["password"]):
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    token_data = {"sub": user["email"], "role": user["role"]}
    access_token = create_access_token(token_data)
    refresh_token = create_refresh_token(token_data)
    
    logger.info("user_logged_in", email=payload.email)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(payload: RefreshTokenRequest):
    try:
        decoded = decode_token(payload.refresh_token)
        if decoded.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid refresh token")
        
        email = decoded.get("sub")
        role = decoded.get("role", "Recruiter")
        
        token_data = {"sub": email, "role": role}
        access_token = create_access_token(token_data)
        new_refresh_token = create_refresh_token(token_data)
        
        return {
            "access_token": access_token,
            "refresh_token": new_refresh_token,
            "token_type": "bearer"
        }
    except Exception as e:
        logger.error("token_refresh_failed", error=str(e))
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
