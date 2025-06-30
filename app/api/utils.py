import httpx
from smtplib import SMTP
from pathlib import Path
import tempfile
from app.settings.base import settings
from email.message import EmailMessage

async def download_from_drive(id_archivo: str, nombre: str) -> Path:
    url = f"https://drive.google.com/uc?export=download&id={id_archivo}"
    async with httpx.AsyncClient() as client:
        r = await client.get(url)
        if r.status_code == 200:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf")
            tmp.write(r.content)
            tmp.flush()
            return tmp.name
        else:
            raise Exception("No se pudo descargar el archivo")
        

def send_to_my_email(name: str, user_email: str, message: str):
    remitente = "sfraustoz.dev@gmail.com"
    destinatario = remitente  # te lo envías a ti mismo

    msg = EmailMessage()
    msg["Subject"] = "Nuevo mensaje de tu portafolio"
    msg["From"] = remitente
    msg["To"] = destinatario
    msg.set_content(f"""
    Nombre: {name}
    Correo: {user_email}

    Mensaje:
    {message}
    """)

    try:
        with SMTP("smtp.gmail.com", 587) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(remitente, settings.smtp_password.get_secret_value())
            server.send_message(msg)
    except Exception as e:
        raise