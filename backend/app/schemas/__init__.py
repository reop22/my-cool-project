# ПУТЬ: backend/app/schemas/__init__.py

from .token import Token, TokenData
from .role import Role, RoleCreate, RoleBase
from .user import User, UserCreate, UserUpdate, UserBase

# --- ФИНАЛЬНЫЙ, ПОЛНЫЙ СПИСОК ИМПОРТОВ ---
from .trip_sheet import (
    TripSheet,
    TripSheetCreate,
    TripSheetUpdatePreTripMedical,
    TripSheetUpdatePostTripMedical, 
    TripSheetUpdatePreTripTechnical,
    TripSheetUpdatePostTripTechnical,
    TripSheetUpdateDispatcherDeparture,
    TripSheetUpdateDispatcherArrival, 
    TripSheetUpdateDriverReturn,
    TripSheetUpdateAdminFinal,
    TripSheetAdminReturnForCorrection,
    TripSheetReturnByPerformer,
    RoutePoint
)