# ПУТЬ: backend/app/models/user.py
from sqlalchemy import String, Boolean, inspect
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
# --- ИМПОРТИРУЕМ TripSheet ДЛЯ TYPE HINTING И RELATIONSHIP ---
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .trip_sheet import TripSheet

class User(Base):
    __tablename__ = "users"
    username: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    full_name: Mapped[str | None] = mapped_column(String)
    hashed_password: Mapped[str] = mapped_column(String, nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    roles = relationship("Role", secondary="user_roles", back_populates="users")

    # --- ДОБАВЛЯЕМ СВЯЗЬ ---
    # Это позволит нам легко получать все путевые листы, где этот пользователь был водителем
    driven_trip_sheets: Mapped[list["TripSheet"]] = relationship(back_populates="driver", foreign_keys="[TripSheet.driver_id]")
    
    def __repr__(self):
        insp = inspect(self)
        if 'roles' not in insp.unloaded:
            role_names = ", ".join([role.name for role in self.roles])
            return f"{self.full_name or self.username} ({role_names or 'Без роли'})"
        else:
            return f"{self.full_name or self.username}"