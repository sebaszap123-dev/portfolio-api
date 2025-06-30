from sqladmin import ModelView
from app.database.models.portfolio import Experience, Project, Certification


class ExperienceAdmin(ModelView, model=Experience):
    column_list = [
        Experience.id,
        Experience.title,
        Experience.company,
        Experience.start_date,
        Experience.end_date,
        Experience.is_current,
        Experience.employment_type,
        Experience.description,
        Experience.technologies,
    ]
    column_searchable_list = [Experience.title, Experience.company]
    column_sortable_list = [
        Experience.start_date,
        Experience.end_date,
        Experience.is_current,
    ]
    form_excluded_columns = []
    form_args = {
        "employment_type": {
            "description": "Remote, Hybrid, On-site, etc.",
        },
        "is_current": {
            "description": "Is my current Job.",
        },
    }


class ProjectAdmin(ModelView, model=Project):
    column_list = [
        Project.id,
        Project.title,
        Project.description,
        Project.technologies,
        Project.github_url,
        Project.demo_url,
        Project.download_url,
        Project.featured,
        Project.start_date,
        Project.end_date,
    ]
    column_searchable_list = [Project.title]
    column_sortable_list = [Project.start_date, Project.end_date, Project.featured]
    form_excluded_columns = []


class CertificationAdmin(ModelView, model=Certification):
    column_list = [
        Certification.id,
        Certification.title,
        Certification.issuer,
        Certification.issue_date,
        Certification.expiration_date,
        Certification.credential_id,
        Certification.credential_url,
    ]
    column_searchable_list = [Certification.title, Certification.issuer]
    column_sortable_list = [Certification.issue_date, Certification.expiration_date]
    form_excluded_columns = []
