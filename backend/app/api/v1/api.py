# backend/app/api/v1/api.py

from fastapi import APIRouter
from .endpoints import users, auth, trip_sheets, roles 

api_router = APIRouter()
api_router.include_router(auth.router)
api_router.include_router(users.router, prefix="/users")
api_router.include_router(trip_sheets.router, prefix="/trip-sheets")
api_router.include_router(roles.router, prefix="/roles") 