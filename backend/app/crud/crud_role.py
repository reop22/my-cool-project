# file: backend/app/crud/crud_role.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.role import Role
from app.schemas.role import RoleCreate

class CRUDRole:
    async def get_role_by_name(self, db: AsyncSession, *, name: str) -> Role | None:
        """Получение роли по её имени."""
        result = await db.execute(select(Role).filter(Role.name == name))
        return result.scalars().first()

    async def create(self, db: AsyncSession, *, role_in: RoleCreate) -> Role:
        """Создание новой роли."""
        db_role = Role(name=role_in.name)
        db.add(db_role)
        await db.commit()
        await db.refresh(db_role)
        return db_role

role = CRUDRole()