from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioCrear(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    edad: int = Field(ge=0, le=100)
    correo: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)


class UsuarioRespuesta(UsuarioCrear):
    id: int

    model_config = ConfigDict(from_attributes=True)