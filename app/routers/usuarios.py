from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# POST: Crear usuario
@router.post("", response_model=schemas.UsuarioRespuesta)
def crear_usuario(usuario: schemas.UsuarioCrear, db: Session = Depends(get_db)):
    nuevo = models.Usuario(**usuario.model_dump())
    db.add(nuevo)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="El correo ya está registrado")
    db.refresh(nuevo)
    return nuevo


# GET: Listar usuarios
@router.get("", response_model=list[schemas.UsuarioRespuesta])
def obtener_usuarios(db: Session = Depends(get_db)):
    return db.query(models.Usuario).all()


# GET: Consultar un usuario
@router.get("/{usuario_id}", response_model=schemas.UsuarioRespuesta)
def obtener_usuario(usuario_id: int, db: Session = Depends(get_db)):
    usuario = db.get(models.Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


# PUT: Actualizar usuario
@router.put("/{usuario_id}", response_model=schemas.UsuarioRespuesta)
def actualizar_usuario(
    usuario_id: int,
    datos: schemas.UsuarioCrear,
    db: Session = Depends(get_db),
):
    usuario = db.get(models.Usuario, usuario_id)
    if usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")