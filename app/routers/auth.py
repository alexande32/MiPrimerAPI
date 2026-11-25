from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import crear_token, verificar_password

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/login", response_model=schemas.Token)
def login(
    formulario: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    # El formulario estándar llama "username" al campo; aquí es el correo
    usuario = (
        db.query(models.Usuario)
        .filter(models.Usuario.correo == formulario.username)
        .first()
    )

    if usuario is None or not verificar_password(
        formulario.password, usuario.password_hash
    ):
        raise HTTPException(
            status_code=401,
            detail="Correo o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return {"access_token": crear_token(usuario.id), "token_type": "bearer"}