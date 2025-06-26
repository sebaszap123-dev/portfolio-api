# schemas/portfolio.py
from datetime import date
from pydantic import BaseModel
from typing import Optional, List, Union


class ExperienceSchema(BaseModel):
    id: int
    title: str
    company: str
    start_date: date
    end_date: Optional[date]
    is_current: bool
    employment_type: Optional[str]
    description: Optional[str]
    achievements: Optional[Union[List[str], dict]]

    class Config:
        orm_mode = True


class ProjectSchema(BaseModel):
    id: int
    title: str
    description: Optional[str]
    technologies: Optional[Union[List[str], dict]]
    github_url: Optional[str]
    demo_url: Optional[str]
    download_url: Optional[str]
    featured: bool
    start_date: Optional[date]
    end_date: Optional[date]
    live_site: Optional[bool] = False
    details: Optional[str] = None

    class Config:
        orm_mode = True


class CertificationSchema(BaseModel):
    id: int
    title: str
    issuer: str
    issue_date: date
    expiration_date: Optional[date]
    credential_id: Optional[str]
    credential_url: Optional[str]

    class Config:
        orm_mode = True
