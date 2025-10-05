from pydantic import BaseModel
from typing import List

class Reultados(BaseModel):
    resultados: List[str]
