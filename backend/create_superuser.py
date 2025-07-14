# ПУТЬ: backend/create_superuser.py

import asyncio
from getpass import getpass

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.session import SessionLocal
from app.crud import user as crud_user, role as crud_role
from app.schemas import UserCreate, RoleCreate

ADMIN_USERNAME = "admin"
ADMIN_ROLE_NAME = "администратор"

async def create_superuser():
    print("--- Запуск скрипта создания суперпользователя ---")
    db: AsyncSession = SessionLocal()

    try:
        # 1. Получаем или создаем пользователя
        user_to_check = await crud_user.get_user_by_username(db, username=ADMIN_USERNAME)
        
        if not user_to_check:
            print(f"Пользователь '{ADMIN_USERNAME}' не найден, создаем нового.")
            admin_password = getpass("Введите пароль для нового администратора: ")
            user_in = UserCreate(
                username=ADMIN_USERNAME, 
                password=admin_password,
                full_name="Главный Администратор"
            )
            user_to_check = await crud_user.create(db, user_in=user_in)
            print(f"Пользователь '{ADMIN_USERNAME}' успешно создан.")
        else:
            print(f"Пользователь '{ADMIN_USERNAME}' уже существует.")

        # 2. Получаем или создаем роль администратора
        admin_role = await crud_role.get_role_by_name(db, name=ADMIN_ROLE_NAME)
        if not admin_role:
            print(f"Роль '{ADMIN_ROLE_NAME}' не найдена. Создаем ее.")
            admin_role = await crud_role.create(db, role_in=RoleCreate(name=ADMIN_ROLE_NAME))
            print(f"Роль '{ADMIN_ROLE_NAME}' успешно создана.")

        # 3. Проверяем, есть ли у пользователя уже эта роль
        user_role_names = [role.name for role in user_to_check.roles]
        if ADMIN_ROLE_NAME in user_role_names:
            print(f"У пользователя '{ADMIN_USERNAME}' уже есть роль администратора.")
        else:
            print(f"Назначаем роль '{ADMIN_ROLE_NAME}' пользователю '{ADMIN_USERNAME}'...")
            await crud_user.assign_role(db, user_id=user_to_check.id, role_id=admin_role.id)
            print("Роль успешно назначена!")

    finally:
        await db.close()

    print("--- Скрипт завершил работу ---")

if __name__ == "__main__":
    asyncio.run(create_superuser())