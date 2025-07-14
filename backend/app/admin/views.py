# ПУТЬ: backend/app/admin/views.py

from sqladmin import ModelView
from app.models import User, Role, TripSheet

class UserAdmin(ModelView, model=User):
    column_list = ["id", "username", "full_name", "is_active", "roles"]
    column_details_list = [User.id, User.username, User.full_name, User.roles, User.is_active]
    form_columns = [User.username, User.full_name, User.is_active, User.roles]
    column_searchable_list = ["username", "full_name"]
    column_sortable_list = ["id", "username", "is_active"]
    name = "Пользователь"
    name_plural = "Пользователи"
    icon = "fa-solid fa-user"
    can_create = False

class RoleAdmin(ModelView, model=Role):
    column_list = ["id", "name"]
    column_details_list = [Role.id, Role.name, Role.users]
    form_columns = [Role.name]
    name = "Роль"
    name_plural = "Роли"
    icon = "fa-solid fa-shield-halved"

# --- ПОЛНОСТЬЮ ОБНОВЛЕННЫЙ КЛАСС ДЛЯ ПУТЕВЫХ ЛИСТОВ ---
class TripSheetAdmin(ModelView, model=TripSheet):
    # Колонки для отображения в общем списке
    column_list = [
        TripSheet.id,
        TripSheet.sheet_number,
        TripSheet.status,
        TripSheet.driver,
        TripSheet.car_plate,
        TripSheet.creation_date,
    ]

    # Поля для отображения на детальной странице (ИСПОЛЬЗУЕМ НОВЫЕ ИМЕНА)
    column_details_list = [
        # Системная информация
        TripSheet.id,
        TripSheet.sheet_number,
        TripSheet.status,
        TripSheet.creation_date,
        # Участники
        TripSheet.driver,
        TripSheet.pre_trip_doctor,
        TripSheet.post_trip_doctor,
        TripSheet.departure_mechanic,
        TripSheet.arrival_mechanic,
        TripSheet.departure_dispatcher,
        TripSheet.arrival_dispatcher,
        # Данные от водителя
        TripSheet.organization_name,
        TripSheet.car_model,
        TripSheet.car_plate,
        TripSheet.driver_license_number,
        # Данные от врача
        TripSheet.pre_trip_medical_check_time,
        TripSheet.post_trip_medical_check_time,
        # Данные от механика (выезд)
        TripSheet.departure_odometer,
        TripSheet.fuel_balance_start,
        TripSheet.departure_actual_time,
        # Данные от диспетчера
        TripSheet.fuel_issued_liters,
        # Данные по возвращении
        TripSheet.arrival_odometer,
        TripSheet.fuel_balance_end,
        TripSheet.arrival_actual_time,
        TripSheet.route_points,
    ]

    # Отключаем создание и редактирование из админки,
    # так как весь процесс должен идти через API и стейт-машину.
    can_create = False
    can_edit = False

    name = "Путевой лист"
    name_plural = "Путевые листы"
    icon = "fa-solid fa-route"