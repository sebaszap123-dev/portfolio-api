from datetime import timedelta
from fastapi import Request
from jose import jwt, ExpiredSignatureError
from sqladmin.authentication import AuthenticationBackend
from app.settings.base import settings
import pendulum


class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, secret_key: str):
        self.secret_key = secret_key
        super().__init__(secret_key=secret_key)

    def create_access_token(self, data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        if expires_delta:
            expire = pendulum.now(tz=pendulum.UTC) + expires_delta
        else:
            expire = pendulum.now(tz=pendulum.UTC) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm="HS256")
        return encoded_jwt

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")

        if (
            username == settings.admin.username
            and password == settings.admin.password.get_secret_value()
        ):
            # Crear token JWT
            access_token = self.create_access_token(
                data={"sub": username},
                expires_delta=timedelta(minutes=settings.admin.token_expire_minutes),
            )

            # Guardar token en sesión
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
            payload = jwt.decode(token, self.secret_key, algorithms=["HS256"])
            username: str = payload.get("sub")
            if username != settings.admin.username:
                return False
        except ExpiredSignatureError:
            return False

        return True
