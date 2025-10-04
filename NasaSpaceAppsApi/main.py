from fastapi import FastAPI
import csv
from pydantic import BaseModel
import pandas as pd
from ClasesApi.BusquedaEntrada import BusquedaEntrada
from ClasesApi.EntradaDatos import EntradaDatos
from ClasesApi.Resultados import Reultados
from ClasesApi.Busqueda import Busqueda
app = FastAPI()


data = pd.read_csv("SB_publication_PMC.csv")

titulos = data.Title.values.tolist()
links = data.Link.values.tolist()

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

#para iniciarlo  uvicorn main:app --reload
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
async def enter_data(  entradadatos: EntradaDatos):

    datos = [ p for p in titulos if p.startswith(entradadatos.palabra)]
    return Reultados(datos)


@app.post("/busqueda")
async def busqueda(busqueda: BusquedaEntrada):
    buscar = Busqueda()
    buscar.titulo = ""
    buscar.url = ""
    for j in range(0 , len(titulos) -1):
        if titulos[j] == busqueda.titulo:
            buscar.titulo = titulos[j]
            buscar.url = links[j]
    return buscar









