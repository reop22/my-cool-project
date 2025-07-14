# ПУТЬ: backend/app/api/v1/endpoints/users.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
# --- ИСПРАВЛЕНИЕ ЗДЕСЬ: Добавляем импорт AsyncSession ---
from sqlalchemy.ext.asyncio import AsyncSession

from app import crud, models, schemas
from app.dependencies.db import get_db_session
from app.dependencies.auth import get_current_user, role_required

router = APIRouter()

@router.get("/", response_model=List[schemas.User], tags=["users"])
async def read_users(db: AsyncSession = Depends(get_db_session), skip: int = 0, limit: int = 100, current_user: models.User = Depends(role_required(["администратор"]))):
    return await crud.user.get_multi(db, skip=skip, limit=limit)

@router.post("/", response_model=schemas.User, status_code=status.HTTP_201_CREATED, tags=["users"])
async def create_new_user(user_in: schemas.UserCreate, db: AsyncSession = Depends(get_db_session), current_user: models.User = Depends(get_current_user)):
    existing_user = await crud.user.get_user_by_username(db, username=user_in.username)
    if existing_user:
        raise HTTPException(status_code=400, detail="Пользователь с таким именем уже существует.")
    
    is_admin_creating = "администратор" in [r.name for r in current_user.roles]
    new_user = await crud.user.create(db=db, user_in=user_in, is_admin_creation=is_admin_creating)
    
    if new_user is None:
        raise HTTPException(status_code=500, detail="Не удалось создать пользователя.")
    return new_user

@router.get("/me", response_model=schemas.User, tags=["users"])
async def read_users_me(current_user: models.User = Depends(get_current_user)):
    return current_user

@router.put("/{user_id}", response_model=schemas.User, tags=["users"])
async def update_user(user_id: int, user_in: schemas.UserUpdate, db: AsyncSession = Depends(get_db_session), current_user: models.User = Depends(role_required(["администратор"]))):
    db_user = await crud.user.get_user_by_id(db, user_id=user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    updated_user = await crud.user.update(db, db_obj=db_user, obj_in=user_in)
    return updated_user

@router.post("/{user_id}/assign-role", response_model=schemas.User, tags=["users"])
async def assign_role(user_id: int, role_id: int, db: AsyncSession = Depends(get_db_session), current_user: models.User = Depends(role_required(["администратор"]))):
    try:
        user = await crud.user.assign_role(db=db, user_id=user_id, role_id=role_id)
        if user is None: raise HTTPException(status_code=404, detail="Не удалось найти пользователя после обновления")
        return user
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/by-role/", response_model=List[schemas.User], tags=["users"])
async def read_users_by_role(role_name: str, db: AsyncSession = Depends(get_db_session), current_user: models.User = Depends(get_current_user)):
    return await crud.user.get_users_by_role(db=db, role_name=role_name)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db_session), current_user: models.User = Depends(role_required(["администратор"]))):
    if user_id == current_user.id:
        raise HTTPException(status_code=403, detail="Нельзя удалить самого себя.")
    
    user_to_delete = await crud.user.get_user_by_id(db, user_id=user_id)
    if not user_to_delete:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    if user_to_delete.driven_trip_sheets:
        raise HTTPException(status_code=409, detail="Нельзя удалить пользователя, так как за ним закреплены путевые листы.")
        
    deleted_user = await crud.user.remove(db=db, id=user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return