
from pydantic import BaseModel, ConfigDict, EmailStr, Field


class UsuarioBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    edad: int = Field(ge=0, le=120)
    correo: EmailStr

    model_config = ConfigDict(str_strip_whitespace=True)


class UsuarioCrear(UsuarioBase):
    password: str = Field(min_length=8, max_length=72)


class UsuarioActualizar(UsuarioBase):
    pass


class UsuarioRespuesta(UsuarioBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str
