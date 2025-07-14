# file: backend/app/admin/auth.py
from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request
from jose import JWTError, jwt

from app.core import security
from app.core.config import settings
from app.crud import user as user_crud
from app.db.session import SessionLocal

class AdminAuth(AuthenticationBackend):
    async def login(self, request: Request) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]

        async with SessionLocal() as db:
            user = await user_crud.authenticate(db, username=username, password=password)
        
        if user and any(role.name == 'администратор' for role in user.roles):
            access_token = security.create_access_token(user.username)
            request.session.update({"token": access_token})
            return True

        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        token = request.session.get("token")

        if not token:
            return False

        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str | None = payload.get("sub")
            if username is None:
                return False
        except JWTError:
            return False
        
        return True

authentication_backend = AdminAuth(secret_key=settings.SECRET_KEY)