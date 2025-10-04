from fastapi import FastAPI
import csv

from ClasesApi.EntradaDatos import EntradaDatos
from ClasesApi.Resultados import Reultados
app = FastAPI()

with open("SB_publication_PMC.csv") as file:
    reader = csv.reader(file)
    header = next(reader)
    data_rows = [row for row in header]



@app.get("/")
async def root():
    return {"message": "Hello World"}
#uvicorn main:app --reload

@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


@app.get("/prueba")
async def prueba():
    palabras = []
    palabras.append("holla")
    palabras.append("hola")
    palabras.append("cola")
    p = Reultados(palabras)
    return p


