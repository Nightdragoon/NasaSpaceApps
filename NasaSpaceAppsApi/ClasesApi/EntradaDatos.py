import pydantic
from pydantic import BaseModel

class EntradaDatos(BaseModel):
    palabra: str