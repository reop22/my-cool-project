# ПУТЬ: backend/app/api/v1/endpoints/trip_sheets.py
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.responses import StreamingResponse

from app import crud, schemas
from app.dependencies.db import get_db_session
from app.services.document_generator import generate_trip_sheet_docx
from app.dependencies.auth import role_required, get_current_user
from app.models import User
from app.models.trip_sheet import TripSheetStatus

router = APIRouter()

# --- ЭНДПОИНТЫ ДЛЯ ЧТЕНИЯ ДАННЫХ ---
@router.get("/", response_model=List[schemas.TripSheet], tags=["trip_sheets"])
async def read_trip_sheets_by_status(db: AsyncSession = Depends(get_db_session), status: TripSheetStatus = Query(...), current_user: User = Depends(get_current_user), skip: int = 0, limit: int = 100):
    return await crud.trip_sheet.get_multi_by_status_for_user(db, status=status, user=current_user, skip=skip, limit=limit)

@router.get("/{sheet_id}", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def read_trip_sheet_by_id(sheet_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if not sheet: raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Путевой лист не найден")
    return sheet

# --- ЭНДПОИНТЫ ДЛЯ ИЗМЕНЕНИЯ ДАННЫХ ПО ЭТАПАМ ---
@router.post("/", response_model=schemas.TripSheet, status_code=status.HTTP_201_CREATED, tags=["trip_sheets"])
async def create_trip_sheet(sheet_in: schemas.TripSheetCreate, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["водитель"]))):
    return await crud.trip_sheet.create_with_driver(db=db, obj_in=sheet_in, driver_id=current_user.id)

@router.patch("/{sheet_id}/submit-for-medical", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def submit_for_medical(
    sheet_id: int,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(role_required(["водитель", "администратор"])),
):
    """[ЭТАП 1.5] Водитель подтверждает черновик и отправляет на медосмотр."""
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.CREATED_BY_DRIVER:
        raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа для этого действия.")
    if sheet.driver_id != current_user.id and "администратор" not in [r.name for r in current_user.roles]:
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Это не ваш путевой лист.")
    return await crud.trip_sheet.submit_for_medical(db=db, db_obj=sheet)

@router.patch("/{sheet_id}/pre-trip-medical", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_pre_trip_medical(sheet_id: int, sheet_in: schemas.TripSheetUpdatePreTripMedical, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["доктор", "администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.AWAITING_PRE_TRIP_MEDICAL: raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа")
    return await crud.trip_sheet.update_pre_trip_medical(db=db, db_obj=sheet, obj_in=sheet_in, doctor_id=current_user.id)

@router.patch("/{sheet_id}/pre-trip-technical", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_pre_trip_technical(sheet_id: int, sheet_in: schemas.TripSheetUpdatePreTripTechnical, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["механик", "администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.AWAITING_PRE_TRIP_TECHNICAL: raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа")
    return await crud.trip_sheet.update_pre_trip_technical(db=db, db_obj=sheet, obj_in=sheet_in, mechanic_id=current_user.id)

@router.patch("/{sheet_id}/dispatcher-departure", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_dispatcher_departure(sheet_id: int, sheet_in: schemas.TripSheetUpdateDispatcherDeparture, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["дежурный", "администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.AWAITING_DISPATCHER_DEPARTURE: raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа")
    return await crud.trip_sheet.update_dispatcher_departure(db=db, db_obj=sheet, obj_in=sheet_in, dispatcher_id=current_user.id)

@router.patch("/{sheet_id}/driver-return", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_driver_return(sheet_id: int, sheet_in: schemas.TripSheetUpdateDriverReturn, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["водитель", "администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.IN_PROGRESS: raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа")
    if sheet.driver_id != current_user.id and "администратор" not in [r.name for r in current_user.roles]: raise HTTPException(status.HTTP_403_FORBIDDEN, "Это не ваш путевой лист.")
    return await crud.trip_sheet.update_driver_return(db=db, db_obj=sheet, obj_in=sheet_in)

@router.patch("/{sheet_id}/post-trip-medical", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_post_trip_medical(sheet_id: int, sheet_in: schemas.TripSheetUpdatePostTripMedical, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["доктор", "администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.AWAITING_POST_TRIP_MEDICAL: raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа")
    return await crud.trip_sheet.update_post_trip_medical(db=db, db_obj=sheet, obj_in=sheet_in, doctor_id=current_user.id)

@router.patch("/{sheet_id}/post-trip-technical", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_post_trip_technical(sheet_id: int, sheet_in: schemas.TripSheetUpdatePostTripTechnical, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["механик", "администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.AWAITING_POST_TRIP_TECHNICAL: raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа")
    return await crud.trip_sheet.update_post_trip_technical(db=db, db_obj=sheet, obj_in=sheet_in, mechanic_id=current_user.id)
    
@router.patch("/{sheet_id}/dispatcher-arrival", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_dispatcher_arrival(sheet_id: int, sheet_in: schemas.TripSheetUpdateDispatcherArrival, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["дежурный", "администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.AWAITING_DISPATCHER_ARRIVAL: raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа")
    return await crud.trip_sheet.update_dispatcher_arrival(db=db, db_obj=sheet, obj_in=sheet_in, dispatcher_id=current_user.id)
    
# --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
@router.patch("/{sheet_id}/admin-final", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def update_admin_final(sheet_id: int, sheet_in: schemas.TripSheetUpdateAdminFinal, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    if sheet.status != TripSheetStatus.COMPLETED: raise HTTPException(status.HTTP_409_CONFLICT, "Путевой лист еще не завершен полностью.")
    return await crud.trip_sheet.update_admin_final(db=db, db_obj=sheet, obj_in=sheet_in)

@router.patch("/{sheet_id}/return-for-correction", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def return_for_correction(sheet_id: int, sheet_in: schemas.TripSheetAdminReturnForCorrection, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["администратор"]))):
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    return await crud.trip_sheet.return_for_correction(db=db, db_obj=sheet, obj_in=sheet_in)

@router.patch("/{sheet_id}/return-by-performer", response_model=schemas.TripSheet, tags=["trip_sheets"])
async def return_by_performer(
    sheet_id: int,
    sheet_in: schemas.TripSheetReturnByPerformer,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(role_required(["доктор", "механик", "администратор"])), # Добавим и админа на всякий случай
):
    """Возвращает путевой лист водителю на доработку (отклонение врачом или механиком)."""
    sheet = await crud.trip_sheet.get_full(db, id=sheet_id)
    
    # Проверка, что отклонить можно только на определенных этапах
    allowed_statuses = [
        TripSheetStatus.AWAITING_PRE_TRIP_MEDICAL,
        TripSheetStatus.AWAITING_PRE_TRIP_TECHNICAL,
        TripSheetStatus.AWAITING_POST_TRIP_MEDICAL
    ]
    if sheet.status not in allowed_statuses:
        raise HTTPException(status.HTTP_409_CONFLICT, "Неверный статус листа для этого действия.")

    return await crud.trip_sheet.return_for_correction_by_performer(db=db, db_obj=sheet, obj_in=sheet_in)

@router.delete("/{sheet_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["trip_sheets"])
async def delete_trip_sheet(sheet_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(role_required(["администратор"]))):
    deleted_sheet = await crud.trip_sheet.remove(db=db, id=sheet_id)
    if not deleted_sheet: raise HTTPException(status.HTTP_404_NOT_FOUND, detail="Путевой лист не найден.")
    return

@router.get("/{sheet_id}/download", tags=["trip_sheets"])
async def download_trip_sheet(sheet_id: int, db: AsyncSession = Depends(get_db_session), current_user: User = Depends(get_current_user)):
    db_sheet = await crud.trip_sheet.get_full(db=db, id=sheet_id)
    if not db_sheet: raise HTTPException(status_code=404, detail="Путевой лист не найден")
    if db_sheet.status != TripSheetStatus.READY_FOR_DOWNLOAD and "администратор" not in [r.name for r in current_user.roles]:
        raise HTTPException(status_code=403, detail="Документ еще не готов к скачиванию.")
    file_stream = generate_trip_sheet_docx(db_sheet)
    file_name = f"trip_sheet_{db_sheet.sheet_number}.docx"
    headers = {'Content-Disposition': f'attachment; filename="{file_name}"'}
    return StreamingResponse(file_stream, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers=headers)