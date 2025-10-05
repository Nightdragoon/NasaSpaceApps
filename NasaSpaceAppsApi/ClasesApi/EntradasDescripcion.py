from pydantic import BaseModel
class EntradasDescripcion(BaseModel):
    titulo: str
    url: str