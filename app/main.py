from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.admin.admin import setup_admin
from app.api.middleware import setup_cors
from app.database.database import Base, engine
from app.api.router import router as main_router


app = FastAPI(title="Async FastAPI with SQLite and Redis")
app.include_router(main_router)
setup_cors(app)
admin = setup_admin(app, engine)
