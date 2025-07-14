# ПУТЬ: backend/app/services/document_generator.py

import io
from pathlib import Path
from docxtpl import DocxTemplate
from datetime import datetime
from app.models.trip_sheet import TripSheet

# Определяем корневую директорию и путь к шаблонам
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
TEMPLATE_DIR = ROOT_DIR / "templates"

def format_dt(dt: datetime | None, fmt: str) -> str:
    """Вспомогательная функция для безопасного форматирования даты и времени."""
    if not dt:
        return ""
    return dt.strftime(fmt)

def generate_trip_sheet_docx(trip_sheet: TripSheet) -> io.BytesIO:
    """Генерирует DOCX файл путевого листа из нового, детализированного шаблона."""
    
    # --- ИСПОЛЬЗУЕМ НОВЫЙ ШАБЛОН ---
    template_path = TEMPLATE_DIR / "detailed_trip_sheet_template.docx"
    
    if not template_path.exists():
        raise FileNotFoundError(f"Шаблон не найден по пути: {template_path}")
        
    try:
        doc = DocxTemplate(template_path)
    except Exception as e:
        raise ValueError(f"Не удалось прочитать шаблон Word: {e}")

    # --- ГОТОВИМ КОНТЕКСТ СО ВСЕМИ НОВЫМИ ПОЛЯМИ ---
    context = {
        'series': trip_sheet.series or "",
        'sheet_number': trip_sheet.sheet_number or "",
        'creation_date_day': format_dt(trip_sheet.creation_date, "%d"),
        'creation_date_month': format_dt(trip_sheet.creation_date, "%m"),
        'creation_date_year': format_dt(trip_sheet.creation_date, "%Y"),
        
        'organization_name': trip_sheet.organization_name or "",
        'organization_address': trip_sheet.organization_address or "",
        'organization_okpo': trip_sheet.organization_okpo or "",
        'form_okud': trip_sheet.form_okud or "",

        'car_model': trip_sheet.car_model or "",
        'car_plate': trip_sheet.car_plate or "",
        'garage_number': trip_sheet.garage_number or "",
        
        'driver_fio': trip_sheet.driver.full_name if trip_sheet.driver else "",
        'driver_personnel_number': trip_sheet.driver_personnel_number or "",
        'driver_license_number': trip_sheet.driver_license_number or "",
        'driver_class': trip_sheet.driver_class or "",
        'driver_snils': trip_sheet.driver_snils or "",

        'transportation_type': trip_sheet.transportation_type or "",
        
        'pre_trip_medical_date': format_dt(trip_sheet.pre_trip_medical_check_time, "%d.%m.%Y"),
        'pre_trip_medical_time': format_dt(trip_sheet.pre_trip_medical_check_time, "%H:%M"),
        'pre_trip_doctor_fio': trip_sheet.pre_trip_doctor.full_name if trip_sheet.pre_trip_doctor else "",
        
        'post_trip_medical_date': format_dt(trip_sheet.post_trip_medical_check_time, "%d.%m.%Y"),
        'post_trip_medical_time': format_dt(trip_sheet.post_trip_medical_check_time, "%H:%M"),
        'post_trip_doctor_fio': trip_sheet.post_trip_doctor.full_name if trip_sheet.post_trip_doctor else "",
        
        'assignment_organization_to': trip_sheet.assignment_organization_to or "",
        'assignment_address': trip_sheet.assignment_address or "",
        
        'departure_mechanic_fio': trip_sheet.departure_mechanic.full_name if trip_sheet.departure_mechanic else "",
        'departure_odometer': trip_sheet.departure_odometer or "",
        'departure_actual_date': format_dt(trip_sheet.departure_actual_time, "%d.%m.%Y"),
        'departure_actual_time': format_dt(trip_sheet.departure_actual_time, "%H:%M"),
        
        'arrival_mechanic_fio': trip_sheet.arrival_mechanic.full_name if trip_sheet.arrival_mechanic else "",
        'arrival_odometer': trip_sheet.arrival_odometer or "",
        
        'fuel_brand': trip_sheet.fuel_brand or "",
        'fuel_code': trip_sheet.fuel_code or "",
        'fuel_issued_liters': trip_sheet.fuel_issued_liters or "0",
        'fuel_balance_start': trip_sheet.fuel_balance_start or "0",
        'fuel_balance_end': trip_sheet.fuel_balance_end or "0",
        'fuel_consumption_norm': trip_sheet.fuel_consumption_norm or "0",
        'fuel_consumption_actual': trip_sheet.fuel_consumption_actual or "0",
        'fuel_saving': trip_sheet.fuel_saving or "0",
        'fuel_overconsumption': trip_sheet.fuel_overconsumption or "0",

        'departure_dispatcher_fio': trip_sheet.departure_dispatcher.full_name if trip_sheet.departure_dispatcher else "",
        'departure_scheduled_date': format_dt(trip_sheet.departure_scheduled_time, "%d.%m.%Y"),
        'departure_scheduled_time_hm': format_dt(trip_sheet.departure_scheduled_time, "%H:%M"),

        'arrival_dispatcher_fio': trip_sheet.arrival_dispatcher.full_name if trip_sheet.arrival_dispatcher else "",
        'arrival_scheduled_date': format_dt(trip_sheet.arrival_scheduled_time, "%d.%m.%Y"),
        'arrival_scheduled_time_hm': format_dt(trip_sheet.arrival_scheduled_time, "%H:%M"),
        'arrival_actual_date': format_dt(trip_sheet.arrival_actual_time, "%d.%m.%Y"),
        'arrival_actual_time_hm': format_dt(trip_sheet.arrival_actual_time, "%H:%M"),

        'idle_time_details': trip_sheet.idle_time_details or "",
        
        # Передаем список словарей для таблицы на оборотной стороне
        'route_points': trip_sheet.route_points or [],
    }

    doc.render(context)

    file_stream = io.BytesIO()
    doc.save(file_stream)
    file_stream.seek(0)

    return file_stream