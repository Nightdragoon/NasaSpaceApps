import pydantic
from pydantic import BaseModel

class Usuario( BaseModel):
    contraseña: str
    usuario: str
    edad: int
    sexo: str
    id_ocupacion: int
