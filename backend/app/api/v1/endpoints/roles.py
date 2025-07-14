from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app import schemas, models
from app.dependencies.db import get_db_session
from app.dependencies.auth import role_required # Защитим эндпоинт

router = APIRouter()

@router.get("/", response_model=List[schemas.Role], tags=["roles"])
async def read_roles(
    db: AsyncSession = Depends(get_db_session),
    # Доступ к списку ролей дадим только администраторам
    current_user: models.User = Depends(role_required(["администратор"]))
):
    """
    Получить список всех доступных ролей в системе.
    """
    query = select(models.Role)
    result = await db.execute(query)
    roles = result.scalars().all()
    return roles