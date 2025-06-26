import asyncio
from logging.config import fileConfig

from sqlalchemy.ext.asyncio import async_engine_from_config
from sqlalchemy.ext.asyncio import AsyncEngine

from alembic import context

from app.settings.base import settings
from app.database.models.base import Base
from app.database.models.portfolio import Experience, Project, Certification

# Config Alembic
config = context.config

# Override .ini url con settings (si lo deseas)
config.set_main_option("sqlalchemy.url", settings.database.url)  # async URL

# Logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata de modelos
target_metadata = Base.metadata


def run_migrations_offline() -> None:
    """Migrations en modo offline."""
    context.configure(
        url=settings.database.sync_url,  # importante: usa URL sync en modo offline
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations_online():
    """Migrations en modo async."""
    connectable: AsyncEngine = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=None,
        future=True,
    )

    async with connectable.begin() as connection:
        await connection.run_sync(
            lambda conn: context.configure(
                connection=conn,
                target_metadata=target_metadata,
            )
        )
        await connection.run_sync(lambda conn: context.run_migrations())


def run_migrations_online() -> None:
    """Wrapper para correr las async migrations"""
    asyncio.run(run_async_migrations_online())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
