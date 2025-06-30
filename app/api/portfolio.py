# routes/portfolio.py
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.database import get_db
from app.database.models.portfolio import Experience, Project, Certification
from app.api.schema.portfolio import (
    ExperienceSchema,
    ProjectSchema,
    CertificationSchema,
)
from sqlalchemy.future import select
from typing import List

router = APIRouter(tags=["Portfolio"])


@router.get("/experiences", response_model=List[ExperienceSchema])
async def get_experiences(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Experience))
    return result.scalars().all()


@router.get("/projects", response_model=List[ProjectSchema])
async def get_projects(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Project))
    return result.scalars().all()


@router.get("/certifications", response_model=List[CertificationSchema])
async def get_certifications(session: AsyncSession = Depends(get_db)):
    result = await session.execute(select(Certification))
    return result.scalars().all()