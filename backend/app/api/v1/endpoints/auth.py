# file: backend/app/api/v1/endpoints/auth.py
from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from app import crud, schemas
from app.core import security
from app.core.config import settings
from app.dependencies.db import get_db_session

router = APIRouter()

@router.post("/login/token", response_model=schemas.Token, tags=["auth"])
async def login_for_access_token(db: AsyncSession = Depends(get_db_session), form_data: OAuth2PasswordRequestForm = Depends()):
    user = await crud.user.authenticate(db, username=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Неверное имя пользователя или пароль")
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = security.create_access_token(
        subject=user.username, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}