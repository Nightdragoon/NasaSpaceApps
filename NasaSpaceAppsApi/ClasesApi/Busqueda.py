import pydantic
from pydantic import BaseModel

class Busqueda(BaseModel):
    titulo: str
    url: str
    description: str
    