from fastapi import FastAPI
from sqladmin import Admin
from sqlalchemy.ext.asyncio import AsyncEngine
from app.admin.views import CertificationAdmin, ExperienceAdmin, ProjectAdmin
from app.auth.security import AdminAuthBackend
from app.settings.base import settings


def setup_admin(app: FastAPI, engine: AsyncEngine):
    # Configurar el backend de autenticación
    auth_backend = AdminAuthBackend(
        secret_key=settings.admin.secret_key.get_secret_value()
    )

    # Crear instancia de Admin
    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=auth_backend,
        title="Admin Panel",
        base_url="/admin",
    )
    admin.add_view(ExperienceAdmin)
    admin.add_view(ProjectAdmin)
    admin.add_view(CertificationAdmin)
    return admin
