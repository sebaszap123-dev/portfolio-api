from contextlib import asynccontextmanager
from fastapi import FastAPI
from app.admin.admin import setup_admin
from app.api.middleware import setup_cors
from app.database.database import Base, engine
from app.cache.cache import redis_client
from app.api.router import router as main_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    # Test Redis connection
    await redis_client.ping()
    print("Redis connected successfully")
    yield  # This separates startup and shutdown logic


app = FastAPI(title="Async FastAPI with SQLite and Redis", lifespan=lifespan)
app.include_router(main_router)
setup_cors(app)
admin = setup_admin(app, engine)
