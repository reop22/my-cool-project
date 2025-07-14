# ПУТЬ: backend/app/crud/crud_user.py
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app.models.user import User as UserModel
from app.models.role import Role as RoleModel
from app.schemas.user import UserCreate, UserUpdate # <-- Добавляем UserUpdate
from app.core.security import get_password_hash, verify_password

class CRUDUser:
    async def get_user_by_id(self, db: AsyncSession, *, user_id: int) -> UserModel | None:
        query = select(UserModel).options(selectinload(UserModel.roles)).where(UserModel.id == user_id)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_user_by_username(self, db: AsyncSession, *, username: str) -> UserModel | None:
        query = select(UserModel).options(selectinload(UserModel.roles)).filter(UserModel.username == username)
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi(self, db: AsyncSession, *, skip: int = 0, limit: int = 100) -> List[UserModel]:
        query = select(UserModel).options(selectinload(UserModel.roles)).order_by(UserModel.id).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def get_users_by_role(self, db: AsyncSession, *, role_name: str) -> List[UserModel]:
        query = (select(UserModel).join(UserModel.roles).filter(RoleModel.name == role_name).options(selectinload(UserModel.roles)))
        result = await db.execute(query)
        return result.scalars().all()

    async def authenticate(self, db: AsyncSession, *, username: str, password: str) -> UserModel | None:
        user = await self.get_user_by_username(db=db, username=username)
        if not user or not verify_password(password, user.hashed_password):
            return None
        return user

    async def create(self, db: AsyncSession, *, user_in: UserCreate, is_admin_creation: bool = False) -> UserModel:
        # При создании через админку, не назначаем роль "водитель" по умолчанию
        roles = []
        if not is_admin_creation:
            role_query = select(RoleModel).where(RoleModel.name == "водитель")
            result = await db.execute(role_query)
            driver_role = result.scalars().first()
            if not driver_role: raise ValueError("Роль 'водитель' не найдена. Запустите initial_data.script.")
            roles.append(driver_role)
        
        hashed_password = get_password_hash(user_in.password)
        db_user = UserModel(username=user_in.username, full_name=user_in.full_name, hashed_password=hashed_password, roles=roles)
        
        db.add(db_user)
        await db.commit()
        await db.refresh(db_user)
        return await self.get_user_by_id(db, user_id=db_user.id)

    async def update(self, db: AsyncSession, *, db_obj: UserModel, obj_in: UserUpdate) -> UserModel: # <-- НОВЫЙ МЕТОД
        update_data = obj_in.model_dump(exclude_unset=True)
        if "password" in update_data and update_data["password"]:
            hashed_password = get_password_hash(update_data["password"])
            del update_data["password"]
            db_obj.hashed_password = hashed_password
        
        for field, value in update_data.items():
            setattr(db_obj, field, value)
            
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def remove(self, db: AsyncSession, *, id: int) -> UserModel | None: # <-- НОВЫЙ МЕТОД
        result = await db.execute(select(UserModel).where(UserModel.id == id))
        db_obj = result.scalars().first()
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

    async def assign_role(self, db: AsyncSession, *, user_id: int, role_id: int) -> UserModel:
        user = await self.get_user_by_id(db, user_id=user_id)
        new_role = await db.get(RoleModel, role_id)
        if not user or not new_role: raise ValueError("Пользователь или роль не найдены")
        user.roles = [new_role]
        db.add(user)
        await db.commit()
        return await self.get_user_by_id(db, user_id=user_id)

user = CRUDUser()