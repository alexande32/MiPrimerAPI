from fastapi import FastAPI

from app import models
from app.database import Base, engine
from app.routers import usuarios

# Crear las tablas si no existen
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mi Primera API",
    description="API desarrollada con Python y FastAPI",
    version="1.0.0"
)

app.include_router(usuarios.router)


@app.get("/")
def inicio():
    return {
        "mensaje": "Bienvenido a mi API",
        "estado": "Funcionando correctamente"
    }


@app.get("/informacion")
def informacion():
    return {
        "nombre": "MiPrimeraAPI",
        "lenguaje": "Python",
        "framework": "FastAPI"
    }


@app.get("/saludo/{nombre}")
def saludo(nombre: str):
    return {"mensaje": f"Hola {nombre}, bienvenido a mi API"}