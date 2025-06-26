from sqlalchemy import Column, Integer, String, Boolean, Date, JSON
from app.database.models.base import Base


class Experience(Base):
    __tablename__ = "experiences"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    company = Column(String(100), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date)
    is_current = Column(Boolean, default=False)
    employment_type = Column(String(50), comment='"Remote", "Hybrid", "On-site", etc.')
    description = Column(String(500))
    achievements = Column(JSON)  # Almacena la lista de logros como JSON

    def __repr__(self):
        return f"<Experience(title='{self.title}', company='{self.company}')>"


class Project(Base):
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)
    description = Column(String(500))
    technologies = Column(JSON)  # Lista de tecnologías como JSON
    github_url = Column(String(200), nullable=True, server_default="")
    demo_url = Column(String(200), nullable=True, server_default="")
    live_site = Column(Boolean(), default=False)
    download_url = Column(
        String(200), nullable=True, server_default=""
    )  # Para APK o archivos descargables
    featured = Column(Boolean, default=False)
    start_date = Column(Date)
    end_date = Column(Date)
    details = Column(String(800), nullable=True, server_default="")

    def __repr__(self):
        return f"<Project(title='{self.title}')>"


class Certification(Base):
    __tablename__ = "certifications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    issuer = Column(String(100), nullable=False)  # Ej: "IBM via Coursera"
    issue_date = Column(Date, nullable=False)
    expiration_date = Column(Date)
    credential_id = Column(String(100))  # ID o número de certificación
    credential_url = Column(String(200))  # URL para verificar la certificación

    def __repr__(self):
        return f"<Certification(title='{self.title}', issuer='{self.issuer}')>"
