import os
from datetime import datetime, timedelta, timezone

import jwt
from jwt.exceptions import InvalidTokenError
from dotenv import load_dotenv
from pwdlib import PasswordHash

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import models
from app.database import get_db
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
MINUTOS_EXPIRACION = 30

if not SECRET_KEY:
    raise RuntimeError("Falta SECRET_KEY en el archivo .env")

hasher = PasswordHash.recommended()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


def hashear_password(password: str) -> str:
    return hasher.hash(password)


def verificar_password(password: str, hash_guardado: str) -> bool:
    return hasher.verify(password, hash_guardado)


def crear_token(usuario_id: int) -> str:
    expira = datetime.now(timezone.utc) + timedelta(minutes=MINUTOS_EXPIRACION)
    datos = {"sub": str(usuario_id), "exp": expira}
    return jwt.encode(datos, SECRET_KEY, algorithm=ALGORITHM)
def obtener_usuario_actual(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar el token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        datos = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = datos.get("sub")

        if usuario_id is None:
            raise error

        usuario_id = int(usuario_id)

    except (InvalidTokenError, ValueError, TypeError):
        raise error

    usuario = db.get(models.Usuario, usuario_id)

    if usuario is None:
        raise error

    return usuario

