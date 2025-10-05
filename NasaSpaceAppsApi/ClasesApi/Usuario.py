import pydantic
from pydantic import BaseModel

class Usuario( BaseModel):
    contrasena: str
    usuario: str
