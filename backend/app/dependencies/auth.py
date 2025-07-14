# file: backend/app/dependencies/auth.py
from typing import List
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.crud import user as user_crud
from app.models import User
from app.dependencies.db import get_db_session

# Эта схема указывает FastAPI, откуда брать токен - из заголовка Authorization
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/login/token")

async def get_current_user(
    token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db_session)
) -> User:
    """
    Декодирует токен, проверяет его и возвращает текущего пользователя из БД.
    Если токен невалидный - выбрасывает исключение.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Не удалось проверить учетные данные",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str | None = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = await user_crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

def role_required(required_roles: List[str]):
    """
    Фабрика зависимостей, которая проверяет, есть ли у пользователя хотя бы одна из требуемых ролей.
    """
    async def check_user_role(current_user: User = Depends(get_current_user)) -> User:
        user_roles = {role.name for role in current_user.roles}
        if not any(role in user_roles for role in required_roles):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Недостаточно прав. Требуется одна из ролей: {required_roles}",
            )
        return current_user
    
    return check_user_role