from pydantic import BaseModel

class BusquedaResultado(BaseModel):
    titulo: str
    url: str