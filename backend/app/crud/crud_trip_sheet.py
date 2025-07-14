# ПУТЬ: backend/app/crud/crud_trip_sheet.py
from datetime import datetime
from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm import selectinload

from app import schemas, models
from app.models.trip_sheet import TripSheetStatus, TripSheet
from app.models.user import User

class CRUDTripSheet:
    async def get_full(self, db: AsyncSession, *, id: int) -> models.TripSheet | None:
        query = (
            select(models.TripSheet)
            .where(models.TripSheet.id == id)
            .options(
                selectinload(models.TripSheet.driver).selectinload(User.roles),
                selectinload(models.TripSheet.pre_trip_doctor).selectinload(User.roles),
                selectinload(models.TripSheet.post_trip_doctor).selectinload(User.roles),
                selectinload(models.TripSheet.assignment_dispatcher).selectinload(User.roles),
                selectinload(models.TripSheet.departure_mechanic).selectinload(User.roles),
                selectinload(models.TripSheet.arrival_mechanic).selectinload(User.roles),
                selectinload(models.TripSheet.departure_dispatcher).selectinload(User.roles),
                selectinload(models.TripSheet.arrival_dispatcher).selectinload(User.roles),
            )
        )
        result = await db.execute(query)
        return result.scalars().first()

    async def get_multi_by_status_for_user(
        self, db: AsyncSession, *, status: TripSheetStatus, user: User, skip: int = 0, limit: int = 100
    ) -> list[models.TripSheet]:
        query = (
            select(models.TripSheet)
            .where(models.TripSheet.status == status)
            .order_by(models.TripSheet.id.desc())
            .options(
                selectinload(models.TripSheet.driver).selectinload(User.roles),
                selectinload(models.TripSheet.pre_trip_doctor).selectinload(User.roles),
                selectinload(models.TripSheet.post_trip_doctor).selectinload(User.roles),
                selectinload(models.TripSheet.assignment_dispatcher).selectinload(User.roles),
                selectinload(models.TripSheet.departure_mechanic).selectinload(User.roles),
                selectinload(models.TripSheet.arrival_mechanic).selectinload(User.roles),
                selectinload(models.TripSheet.departure_dispatcher).selectinload(User.roles),
                selectinload(models.TripSheet.arrival_dispatcher).selectinload(User.roles),
            )
        )
        if "водитель" in [r.name for r in user.roles] and not "администратор" in [r.name for r in user.roles]:
            query = query.where(models.TripSheet.driver_id == user.id)
        query = query.offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all()

    async def create_with_driver(self, db: AsyncSession, *, obj_in: schemas.TripSheetCreate, driver_id: int) -> models.TripSheet:
        sheet_number = f"PL-{int(datetime.now().timestamp())}"
        # Статус по умолчанию 'создан водителем' из модели
        db_obj = models.TripSheet(**obj_in.model_dump(), sheet_number=sheet_number, driver_id=driver_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return await self.get_full(db=db, id=db_obj.id)
    
    # --- НОВЫЙ МЕТОД ---
    async def submit_for_medical(self, db: AsyncSession, *, db_obj: TripSheet) -> TripSheet:
        """
        Водитель подтверждает данные и отправляет лист на медосмотр.
        """
        sheet_id = db_obj.id
        db_obj.status = TripSheetStatus.AWAITING_PRE_TRIP_MEDICAL
        db_obj.rejection_reason = None # Очищаем причину возврата, если она была
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def update_pre_trip_medical(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdatePreTripMedical, doctor_id: int) -> TripSheet:
        sheet_id = db_obj.id
        db_obj.pre_trip_medical_check_time = datetime.now()
        db_obj.pre_trip_doctor_id = doctor_id
        db_obj.pre_trip_doctor_license = obj_in.pre_trip_doctor_license
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.AWAITING_PRE_TRIP_TECHNICAL
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def update_pre_trip_technical(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdatePreTripTechnical, mechanic_id: int) -> TripSheet:
        sheet_id = db_obj.id
        db_obj.departure_odometer = obj_in.departure_odometer
        db_obj.fuel_balance_start = obj_in.fuel_balance_start
        db_obj.pre_trip_control_notes = obj_in.pre_trip_control_notes
        db_obj.departure_mechanic_id = mechanic_id
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.AWAITING_DISPATCHER_DEPARTURE
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def update_dispatcher_departure(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdateDispatcherDeparture, dispatcher_id: int) -> TripSheet:
        sheet_id = db_obj.id
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items(): setattr(db_obj, field, value)
        db_obj.assignment_dispatcher_id = dispatcher_id
        db_obj.departure_dispatcher_id = dispatcher_id
        db_obj.departure_actual_time = datetime.now()
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.IN_PROGRESS
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def update_driver_return(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdateDriverReturn) -> TripSheet:
        sheet_id = db_obj.id
        db_obj.route_points = [point.model_dump() for point in obj_in.route_points]
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.AWAITING_POST_TRIP_MEDICAL
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def update_post_trip_medical(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdatePostTripMedical, doctor_id: int) -> TripSheet:
        sheet_id = db_obj.id
        db_obj.post_trip_medical_check_time = datetime.now()
        db_obj.post_trip_doctor_id = doctor_id
        db_obj.post_trip_doctor_license = obj_in.post_trip_doctor_license
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.AWAITING_POST_TRIP_TECHNICAL
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def update_post_trip_technical(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdatePostTripTechnical, mechanic_id: int) -> TripSheet:
        sheet_id = db_obj.id
        db_obj.arrival_odometer = obj_in.arrival_odometer
        db_obj.fuel_balance_end = obj_in.fuel_balance_end
        db_obj.arrival_mechanic_id = mechanic_id
        db_obj.arrival_actual_time = datetime.now()
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.AWAITING_DISPATCHER_ARRIVAL
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)
    
    async def update_dispatcher_arrival(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdateDispatcherArrival, dispatcher_id: int) -> TripSheet:
        sheet_id = db_obj.id
        db_obj.idle_time_details = obj_in.idle_time_details
        db_obj.arrival_dispatcher_id = dispatcher_id
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.COMPLETED
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)
        
    async def update_admin_final(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetUpdateAdminFinal) -> TripSheet:
        sheet_id = db_obj.id
        if db_obj.fuel_balance_start is not None and db_obj.fuel_balance_end is not None and db_obj.fuel_issued_liters is not None:
            db_obj.fuel_consumption_actual = (db_obj.fuel_balance_start + db_obj.fuel_issued_liters) - db_obj.fuel_balance_end
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items(): setattr(db_obj, field, value)
        db_obj.rejection_reason = None
        db_obj.status = TripSheetStatus.READY_FOR_DOWNLOAD
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def return_for_correction(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetAdminReturnForCorrection) -> TripSheet:
        sheet_id = db_obj.id
        db_obj.status = obj_in.target_status
        db_obj.rejection_reason = obj_in.rejection_reason
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def return_for_correction_by_performer(self, db: AsyncSession, *, db_obj: TripSheet, obj_in: schemas.TripSheetReturnByPerformer) -> TripSheet: # <-- НОВЫЙ МЕТОД
        """
        Возвращает путевой лист на предыдущий этап (к водителю) по причине, указанной исполнителем (врачом или механиком).
        """
        sheet_id = db_obj.id
        db_obj.status = TripSheetStatus.CREATED_BY_DRIVER
        db_obj.rejection_reason = obj_in.rejection_reason
        db.add(db_obj)
        await db.commit()
        return await self.get_full(db=db, id=sheet_id)

    async def remove(self, db: AsyncSession, *, id: int) -> TripSheet | None:
        result = await db.execute(select(TripSheet).where(TripSheet.id == id))
        db_obj = result.scalars().first()
        if db_obj:
            await db.delete(db_obj)
            await db.commit()
        return db_obj

trip_sheet = CRUDTripSheet()