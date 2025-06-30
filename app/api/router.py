from pathlib import Path
from fastapi import APIRouter, Depends, Form, BackgroundTasks
import httpx
from app.api.portfolio import router as general_router
from fastapi.responses import FileResponse

from app.api.schema.portfolio import ContactResponseSchema, ContactSchema
from app.api.utils import download_from_drive, send_to_my_email
from app.auth.api_security import api_key_auth

router = APIRouter(prefix="/api/v1", tags=["Portfolio"], dependencies=[Depends(api_key_auth)])
router.include_router(general_router)

@router.get("/cv/download")
async def download_file():
    ruta = Path("app/media/documents/CV_Frausto.pdf")  # ruta local en tu servidor
    if not ruta.exists():
        return {"error": "Archivo no encontrado"}

    return FileResponse(
        path=ruta,
        filename="cv_frausto.pdf", 
        media_type="application/pdf"
    )

@router.post("/contact", response_model=ContactResponseSchema)
async def contact(
    contact_data: ContactSchema,
    background_tasks: BackgroundTasks
):
    try:
        background_tasks.add_task(
            send_to_my_email, contact_data.name, contact_data.email, contact_data.message
        )
        return {"ok": True, "msg": "Mensaje enviado"}
    except Exception as e:
        return {"ok": False, "msg": str(e)}