from fastapi import FastAPI
import csv
import sqlite3
from pydantic import BaseModel
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from ClasesApi.BusquedaEntrada import BusquedaEntrada
from ClasesApi.EntradaDatos import EntradaDatos
from ClasesApi.Resultados import Reultados
from ClasesApi.Busqueda import Busqueda
from ClasesApi.Usuario import Usuario



app = FastAPI()

engine = create_engine("mysql+pymysql://udxujdjuoiegl6tz:NZ6xcIlGvn44sd4zb5T@bzths6jyaksc7qfl8qpg-mysql.services.clever-cloud.com:20620/bzths6jyaksc7qfl8qpg")

Base = automap_base()

Base.prepare(engine, reflect=True)

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
def enter_data(  entradadatos: EntradaDatos):

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



@app.post("/nuevousuario")
def insert_alumno(usuario: Usuario):
    with sqlite3.connect("bzths6jyaksc7qfl8qpg.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuarios (usuario, contraseña)
            VALUES (?, ?)
        """, (usuario.usuario, usuario.contraseña))
        conn.commit()
    return {
        "message": "Usuario registrado!",
        "data": {
            "usuario": usuario.usuario,
            "id": usuario.id,
        }
    }











