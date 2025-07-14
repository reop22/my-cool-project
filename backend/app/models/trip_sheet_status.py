# ПУТЬ: backend/app/models/trip_sheet_status.py

from enum import Enum

class TripSheetStatus(str, Enum):
    DRAFT = "черновик"
    AWAITING_MEDICAL = "ожидает медосмотра"
    AWAITING_TECHNICAL = "ожидает техосмотра"
    READY_FOR_DISPATCH = "готов к выдаче"
    IN_PROGRESS = "в рейсе"
    COMPLETED = "рейс завершен"
    ARCHIVED = "в архиве"