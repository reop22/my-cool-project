# ПУТЬ: backend/app/initial_data/script.py

import asyncio

from app.crud import role as crud_role
from app.schemas import RoleCreate
from app.db.session import SessionLocal

# --- РАСШИРЯЕМ СПИСОК РОЛЕЙ ---
ROLES = ["водитель", "доктор", "дежурный", "администратор", "механик"]

async def main() -> None:
    print("Запуск скрипта для создания первоначальных данных...")
    db = SessionLocal()
    
    for role_name in ROLES:
        # Проверяем, существует ли уже такая роль
        existing_role = await crud_role.get_role_by_name(db, name=role_name)
        if not existing_role:
            role_in = RoleCreate(name=role_name)
            await crud_role.create(db, role_in=role_in)
            print(f"Роль '{role_name}' успешно создана.")
        else:
            print(f"Роль '{role_name}' уже существует.")

    await db.close()
    print("Скрипт завершил работу.")

if __name__ == "__main__":
    asyncio.run(main())