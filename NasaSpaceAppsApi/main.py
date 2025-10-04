from fastapi import FastAPI
import csv
from pydantic import BaseModel
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine , select , insert , delete, update
from ClasesApi.BusquedaEntrada import BusquedaEntrada
from ClasesApi.EntradaDatos import EntradaDatos
from ClasesApi.Resultados import Reultados
from ClasesApi.Busqueda import Busqueda
from ClasesApi.Usuario import Usuario
from ClasesApi.Historial import Historial
from ClasesApi.HistorialEntrada import HistorialEntrada



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

@app.post("/registeruser")
async def register_user(usuario: Usuario):
    stmt = select(Base.classes.Usuarios).where(Base.classes.Usuarios.usuario == usuario.usuario)
    with engine.connect() as connection:
        result = connection.execute(stmt).first()

        if result:
            return {"message": "Usuario ya existe"}
        else:
            ins = insert(Base.classes.Usuarios).values(usuario=usuario.usuario, contraseña=usuario.contraseña)
            connection.execute(ins)
            connection.commit()
            return {"message": "Usuario registrado exitosamente"}


@app.post("/verifyuser")
async def verify_user(usuario: Usuario):
    stmt = select(Base.classes.Usuarios).where(Base.classes.Usuarios.usuario == usuario.usuario)
    with engine.connect() as connection:
        result = connection.execute(stmt).first()
        
        if result:
            return {"message": "Aqui se dirige al menu principal", "id": result.id}
        else:
            return {"message": "Datos incorrectos"}
            return{ "Message": "Aqui se dirige de nuevo al login"}


@app.post("/insertarHistorial")
async def insertarHistorial(historial: HistorialEntrada):
    stmt = insert(Base.classes.Historial).values(id_usuario=historial.id_usuario , titulo=historial.titulo, url=historial.url)
    with engine.connect() as connection:
        conexion = connection.execute(stmt)
        connection.commit()
    return {"ok":"ok"}
  
@app.get("/historial")
async def historial(id:int):
    historial = []
    stmt = select(Base.classes.Historial).where(Base.classes.Historial.id_usuario == id)
    with engine.connect() as connection:
        for row in  connection.execute(stmt):
            buscar = Busqueda()
            buscar.titulo = row.titulo
            buscar.url = row.url
            historial.append(buscar)

    return Historial(historial)




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














