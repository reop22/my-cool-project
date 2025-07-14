# ПУТЬ: backend/app/schemas/trip_sheet.py
from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional, List
from .user import User
from app.models.trip_sheet import TripSheetStatus

class RoutePoint(BaseModel):
    customer_number: str
    departure_point: str
    arrival_point: str
    departure_time: str
    arrival_time: str
    distance: float
    cargo_weight: Optional[float] = None

class TripSheetCreate(BaseModel):
    series: str
    organization_name: str
    organization_address: str
    organization_okpo: str
    organization_phone: str
    registration_number: str
    communication_type: str
    car_model: str
    car_plate: str
    garage_number: str
    driver_license_number: str
    driver_license_type: str
    driver_class: str
    driver_snils: str
    driver_personnel_number: str

class TripSheetUpdatePreTripMedical(BaseModel):
    pre_trip_doctor_license: str

class TripSheetUpdatePostTripMedical(BaseModel):
    post_trip_doctor_license: str

class TripSheetUpdatePreTripTechnical(BaseModel):
    departure_odometer: int
    fuel_balance_start: float
    pre_trip_control_notes: str

class TripSheetUpdateDispatcherDeparture(BaseModel):
    assignment_organization_to: str
    assignment_address: str
    departure_scheduled_time: datetime
    arrival_scheduled_time: datetime
    fuel_brand: str
    fuel_code: str
    fuel_issued_liters: float

class TripSheetUpdateDriverReturn(BaseModel):
    route_points: List[RoutePoint]

class TripSheetUpdatePostTripTechnical(BaseModel):
    arrival_odometer: int
    fuel_balance_end: float

class TripSheetUpdateDispatcherArrival(BaseModel):
    idle_time_details: str

class TripSheetAdminReturnForCorrection(BaseModel):
    target_status: TripSheetStatus
    rejection_reason: str

class TripSheetReturnByPerformer(BaseModel):
    rejection_reason: str

# --- ИСПРАВЛЕНИЕ ЗДЕСЬ ---
# Класс переименован в TripSheetUpdateAdminFinal
class TripSheetUpdateAdminFinal(BaseModel):
    fuel_consumption_norm: Optional[float] = None
    fuel_consumption_actual: Optional[float] = None
    fuel_saving: Optional[float] = None
    fuel_overconsumption: Optional[float] = None
    work_results_notes: Optional[str] = None
    salary_calculation_notes: Optional[str] = None

class TripSheet(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    sheet_number: str
    creation_date: datetime
    series: Optional[str] = None
    form_okud: Optional[str] = None
    registration_number: Optional[str] = None
    status: TripSheetStatus
    rejection_reason: Optional[str] = None

    organization_name: Optional[str] = None
    organization_address: Optional[str] = None
    organization_phone: Optional[str] = None
    organization_okpo: Optional[str] = None

    car_model: Optional[str] = None
    car_plate: Optional[str] = None
    garage_number: Optional[str] = None

    driver: Optional[User] = None
    driver_license_number: Optional[str] = None
    driver_license_type: Optional[str] = None
    driver_class: Optional[str] = None
    driver_snils: Optional[str] = None
    driver_personnel_number: Optional[str] = None
    
    transportation_type: Optional[str] = None
    communication_type: Optional[str] = None

    pre_trip_medical_check_time: Optional[datetime] = None
    pre_trip_doctor: Optional[User] = None
    pre_trip_doctor_license: Optional[str] = None
    post_trip_medical_check_time: Optional[datetime] = None
    post_trip_doctor: Optional[User] = None
    post_trip_doctor_license: Optional[str] = None

    assignment_dispatcher: Optional[User] = None
    assignment_organization_to: Optional[str] = None
    assignment_address: Optional[str] = None

    fuel_brand: Optional[str] = None
    fuel_code: Optional[str] = None
    fuel_issued_liters: Optional[float] = None
    fuel_balance_start: Optional[float] = None
    fuel_balance_end: Optional[float] = None
    fuel_consumption_norm: Optional[float] = None
    fuel_consumption_actual: Optional[float] = None
    fuel_saving: Optional[float] = None
    fuel_overconsumption: Optional[float] = None

    departure_mechanic: Optional[User] = None
    departure_odometer: Optional[int] = None
    departure_actual_time: Optional[datetime] = None
    pre_trip_control_notes: Optional[str] = None
    
    arrival_mechanic: Optional[User] = None
    arrival_odometer: Optional[int] = None
    arrival_actual_time: Optional[datetime] = None

    departure_dispatcher: Optional[User] = None
    departure_scheduled_time: Optional[datetime] = None
    arrival_dispatcher: Optional[User] = None
    arrival_scheduled_time: Optional[datetime] = None

    idle_time_details: Optional[str] = None
    
    route_points: Optional[List[RoutePoint]] = None
    
    work_results_notes: Optional[str] = None
    salary_calculation_notes: Optional[str] = None