# file: backend/app/db/base.py
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import Column, Integer

class Base:
    # Автоматически добавляем id как первичный ключ ко всем моделям
    id: Mapped[int] = mapped_column(primary_key=True)

Base = declarative_base(cls=Base)