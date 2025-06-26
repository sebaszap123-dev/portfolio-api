# app/dependencies/security.py
from fastapi import Header, HTTPException, status
from app.settings.base import settings


async def api_key_auth(x_api_key: str = Header(...)):
    if x_api_key != settings.api_key.get_secret_value():
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="YOU DONT HAVE AUTHORIZATION TO USE THIS AND IF YOU HAVE PLEASE REPORT IT TO ME :C",
        )
