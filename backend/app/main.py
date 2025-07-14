# file: backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqladmin import Admin

from app.api.v1.api import api_router
from app.db.session import engine 
from app.admin.views import UserAdmin, RoleAdmin, TripSheetAdmin
from app.admin.auth import authentication_backend # <-- Возвращаем защищенную админку

app = FastAPI(title="Digital Dispatcher API")

# Монтируем папку static, чтобы FastAPI мог отдавать из нее файлы, например favicon.ico
# Убедитесь, что папка backend/app/static существует
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Создаем экземпляр админ-панели с аутентификацией
admin = Admin(app, engine, authentication_backend=authentication_backend)

# Регистрируем наши представления в админ-панели
admin.add_view(UserAdmin)
admin.add_view(RoleAdmin)
admin.add_view(TripSheetAdmin)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Digital Dispatcher API"}

app.include_router(api_router, prefix="/api/v1")