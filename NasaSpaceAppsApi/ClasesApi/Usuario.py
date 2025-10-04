import pydantic
from pydantic import BaseModel

class Usuario( BaseModel):
    contraseña: str
    usuario: str
