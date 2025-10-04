from fastapi import FastAPI
import csv
from pydantic import BaseModel
import pandas as pd

from ClasesApi.EntradaDatos import EntradaDatos
from ClasesApi.Resultados import Reultados
from ClasesApi.Busqueda import Busqueda
app = FastAPI()


data = pd.read_csv("SB_publication_PMC.csv")

titulos = data.Title.values.tolist()


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




@app.post("/enterdata")
def enter_data(  entradadatos: EntradaDatos):

    datos = [ p for p in titulos if p.startswith(entradadatos.palabra)]


    coincidencias = [p for p in datos if entradadatos.palabra.lower() in p.lower() ]

    if coincidencias:
        return Reultados(coincidencias) 
    else:
        return None 










