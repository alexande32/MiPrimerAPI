
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app import models, schemas
from app.database import get_db
from app.security import hashear_password, obtener_usuario_actual

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


# POST: Crear usuario (público)
@router.post("", response_model=schemas.UsuarioRespuesta)
def crear_usuario(
    usuario: schemas.UsuarioCrear,
    db: Session = Depends(get_db)
):
    datos = usuario.model_dump()

    nuevo = models.Usuario(
        nombre=datos["nombre"],
        edad=datos["edad"],
        correo=datos["correo"].strip().lower(),
        password_hash=hashear_password(datos["password"])
    )

    db.add(nuevo)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    db.refresh(nuevo)
    return nuevo


# GET: Listar usuarios (protegido)
@router.get("", response_model=list[schemas.UsuarioRespuesta])
def obtener_usuarios(
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    return db.query(models.Usuario).all()


# GET: Consultar un usuario (protegido)
@router.get("/{usuario_id}", response_model=schemas.UsuarioRespuesta)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    usuario = db.get(models.Usuario, usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    return usuario


# PUT: Actualizar usuario (protegido)
@router.put("/{usuario_id}", response_model=schemas.UsuarioRespuesta)
def actualizar_usuario(
    usuario_id: int,
    datos: schemas.UsuarioActualizar,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    usuario = db.get(models.Usuario, usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    usuario.nombre = datos.nombre
    usuario.edad = datos.edad
    usuario.correo = datos.correo.strip().lower()

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail="El correo ya está registrado"
        )

    db.refresh(usuario)
    return usuario


# DELETE: Eliminar usuario (protegido)
@router.delete("/{usuario_id}")
def eliminar_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    usuario_actual: models.Usuario = Depends(obtener_usuario_actual)
):
    usuario = db.get(models.Usuario, usuario_id)

    if usuario is None:
        raise HTTPException(
            status_code=404,
            detail="Usuario no encontrado"
        )

    db.delete(usuario)
    db.commit()

    return {"mensaje": "Usuario eliminado correctamente"}
