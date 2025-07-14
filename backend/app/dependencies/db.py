# file: backend/app/dependencies/db.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal

async def get_db_session() -> AsyncGenerator[AsyncSession, None]:
    """Зависимость для получения сессии базы данных."""
    async with SessionLocal() as session:
        yield session