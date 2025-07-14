# ПУТЬ: backend/app/models/trip_sheet.py

from sqlalchemy import ForeignKey, String, func, JSON, Text
from sqlalchemy.orm import relationship, Mapped, mapped_column
from app.db.base import Base
from datetime import datetime
from enum import Enum

class TripSheetStatus(str, Enum):
    CREATED_BY_DRIVER = "создан водителем"
    AWAITING_PRE_TRIP_MEDICAL = "ожидает предрейсового медосмотра"
    AWAITING_PRE_TRIP_TECHNICAL = "ожидает предрейсового техосмотра"
    AWAITING_DISPATCHER_DEPARTURE = "ожидает выпуска диспетчером"
    IN_PROGRESS = "в рейсе"
    AWAITING_POST_TRIP_MEDICAL = "ожидает послерейсового медосмотра" # <-- НОВЫЙ СТАТУС
    AWAITING_POST_TRIP_TECHNICAL = "ожидает послерейсового техосмотра"
    AWAITING_DISPATCHER_ARRIVAL = "ожидает отметки о возвращении диспетчером"
    COMPLETED = "завершен"
    READY_FOR_DOWNLOAD = "готов к скачиванию" # <-- НОВЫЙ СТАТУС
    ARCHIVED = "в архиве"


class TripSheet(Base):
    __tablename__ = "trip_sheets"

    # --- ОБЩИЕ ДАННЫЕ И ШАПКА ---
    sheet_number: Mapped[str] = mapped_column(unique=True, index=True)
    creation_date: Mapped[datetime] = mapped_column(server_default=func.now())
    series: Mapped[str | None]
    form_okud: Mapped[str | None] = mapped_column(default="74474742")
    registration_number: Mapped[str | None] # <-- НОВОЕ ПОЛЕ
    
    status: Mapped[TripSheetStatus] = mapped_column(String(50), default=TripSheetStatus.CREATED_BY_DRIVER)
    rejection_reason: Mapped[str | None] = mapped_column(Text) # <-- НОВОЕ ПОЛЕ для возврата на доработку

    # --- Раздел "ОРГАНИЗАЦИЯ" ---
    organization_name: Mapped[str | None]
    organization_address: Mapped[str | None]
    organization_phone: Mapped[str | None] # <-- НОВОЕ ПОЛЕ
    organization_okpo: Mapped[str | None]
    
    # --- Раздел "АВТОМОБИЛЬ" ---
    car_model: Mapped[str | None]
    car_plate: Mapped[str | None]
    garage_number: Mapped[str | None]
    
    # --- Раздел "ВОДИТЕЛЬ" ---
    driver_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    driver = relationship("User", foreign_keys=[driver_id], back_populates="driven_trip_sheets")
    driver_license_number: Mapped[str | None]
    driver_license_type: Mapped[str | None] # <-- НОВОЕ ПОЛЕ (стандартная/ограниченная)
    driver_class: Mapped[str | None]
    driver_snils: Mapped[str | None]
    driver_personnel_number: Mapped[str | None]
    
    # --- Раздел "ПЕРЕВОЗКИ" ---
    transportation_type: Mapped[str | None] = mapped_column(default="перевозки для собственных нужд")
    communication_type: Mapped[str | None] # <-- НОВОЕ ПОЛЕ
    
    # --- Раздел "МЕДОСМОТР" (Предрейсовый) ---
    pre_trip_medical_check_time: Mapped[datetime | None]
    pre_trip_doctor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    pre_trip_doctor = relationship("User", foreign_keys=[pre_trip_doctor_id])
    pre_trip_doctor_license: Mapped[str | None] # <-- НОВОЕ ПОЛЕ
    
    # --- Раздел "МЕДОСМОТР" (Послерейсовый) ---
    post_trip_medical_check_time: Mapped[datetime | None]
    post_trip_doctor_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    post_trip_doctor = relationship("User", foreign_keys=[post_trip_doctor_id])
    post_trip_doctor_license: Mapped[str | None] # <-- НОВОЕ ПОЛЕ
    
    # --- Раздел "ЗАДАНИЕ ВОДИТЕЛЮ" ---
    assignment_dispatcher_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    assignment_dispatcher = relationship("User", foreign_keys=[assignment_dispatcher_id])
    assignment_organization_to: Mapped[str | None]
    assignment_address: Mapped[str | None]
    
    # --- Раздел "ДВИЖЕНИЕ ГОРЮЧЕГО" ---
    fuel_brand: Mapped[str | None]
    fuel_code: Mapped[str | None]
    fuel_issued_liters: Mapped[float | None]
    fuel_balance_start: Mapped[float | None]
    fuel_balance_end: Mapped[float | None]
    fuel_consumption_norm: Mapped[float | None]
    fuel_consumption_actual: Mapped[float | None]
    fuel_saving: Mapped[float | None]
    fuel_overconsumption: Mapped[float | None]
    
    # --- Раздел "ТЕХНИЧЕСКИЙ КОНТРОЛЬ" (Выезд) ---
    departure_mechanic_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    departure_mechanic = relationship("User", foreign_keys=[departure_mechanic_id])
    departure_odometer: Mapped[int | None]
    departure_actual_time: Mapped[datetime | None]
    pre_trip_control_notes: Mapped[str | None] # <-- НОВОЕ ПОЛЕ
    
    # --- Раздел "ТЕХНИЧЕСКИЙ КОНТРОЛЬ" (Возвращение) ---
    arrival_mechanic_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    arrival_mechanic = relationship("User", foreign_keys=[arrival_mechanic_id])
    arrival_odometer: Mapped[int | None]
    arrival_actual_time: Mapped[datetime | None]
    
    # --- Раздел "ДИСПЕТЧЕР-НАРЯДЧИК" ---
    departure_dispatcher_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    departure_dispatcher = relationship("User", foreign_keys=[departure_dispatcher_id])
    departure_scheduled_time: Mapped[datetime | None]
    
    arrival_dispatcher_id: Mapped[int | None] = mapped_column(ForeignKey("users.id"))
    arrival_dispatcher = relationship("User", foreign_keys=[arrival_dispatcher_id])
    arrival_scheduled_time: Mapped[datetime | None]
    
    idle_time_details: Mapped[str | None]
    
    route_points: Mapped[dict | None] = mapped_column(JSON)
    
    # --- РАСЧЕТЫ ---
    work_results_notes: Mapped[str | None]
    salary_calculation_notes: Mapped[str | None]