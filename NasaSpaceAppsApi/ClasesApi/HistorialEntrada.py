from pydantic import BaseModel
class HistorialEntrada(BaseModel):
    id_usuario:int
    titulo:str
    url:str