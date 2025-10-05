from fastapi import FastAPI
import csv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import pandas as pd
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine , select , insert , delete, update
from ClasesApi.BusquedaEntrada import BusquedaEntrada
from ClasesApi.EntradaDatos import EntradaDatos
from ClasesApi.EntradasDescripcion import EntradasDescripcion
from ClasesApi.Resultados import Reultados
from ClasesApi.Busqueda import Busqueda
from ClasesApi.Usuario import Usuario
from ClasesApi.Historial import Historial
from ClasesApi.HistorialEntrada import HistorialEntrada

from ClasesApi.Descripcion import  Descripcion
from openai import OpenAI
import requests

from ClasesApi.ArticuloResumen import ArticuloResumen
from ClasesApi.Articulo import Articulo
# OpenAI
from openai import OpenAI

import json


client = OpenAI()


app = FastAPI()

engine = create_engine("mysql+pymysql://udxujdjuoiegl6tz:NZ6xcIlGvn44sd4zb5T@bzths6jyaksc7qfl8qpg-mysql.services.clever-cloud.com:20620/bzths6jyaksc7qfl8qpg")

Base = automap_base()

Base.prepare(engine, reflect=True)

firstatement = select(Base.classes.APIKEY)
api_key = ""

with engine.connect() as connection:
    for row in connection.execute(firstatement):
        api_key = row.api

client =  OpenAI(api_key=api_key)
data = pd.read_csv("SB_publication_PMC.csv")

titulos = data.Title.values.tolist()
links = data.Link.values.tolist()

app = FastAPI()



@app.post("/descripcion")
async def descripcion(descripcion: EntradasDescripcion):
    headers = {
        "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/126.0.0.0 Safari/537.36"),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "es-MX,es;q=0.9,en;q=0.8",
        "Referer": "https://pmc.ncbi.nlm.nih.gov/",
    }
    res = requests.get(url=descripcion.url , headers=headers)

    titulo = descripcion.titulo
    url = descripcion.url
    response = client.responses.create(
        model="gpt-5",
        input="lee esto " + res.text + " y quiero que me hagas una descripcion del articulo solo y unicamente la descripcion  del ariticulo , esta descripcion es creada por ti  no me respondas ni me saludes , solo crea la lee el articulo y crae una corta descripcion"
    )
    return Descripcion(titulo=titulo, url=url , descripcion=response.output_text)



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



@app.post("/resumen")
async def generar_resumen(articulo: Articulo):
    try:
        prompt = f"""
        Basado en los fragmentos de artículos científicos recuperados,
        Título: {articulo.titulo}
        Link: {articulo.link}
        Descripción: {articulo.descripcion}

        Devuelve solo un JSON válido con estas claves:
        {{
            "titulo": "",
            "introduccion_contexto": "",
            "hallazgos_clave": "",
            "conclusion_implicaciones": ""
        }}
        No agregues explicaciones ni texto adicional.
        """

        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "Eres un analista experto en biología espacial."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2
        )

        content = response.choices[0].message.content.strip()

        # Extraer solo el JSON
        import re, json
        json_text = re.search(r'\{.*\}', content, re.DOTALL)
        if not json_text:
            raise HTTPException(status_code=500, detail="La IA no devolvió un JSON válido")
        data = json.loads(json_text.group())

        resumen = ArticuloResumen()
        resumen.titulo = data.get("titulo", "")
        resumen.introduccion_contexto = data.get("introduccion_contexto", "")
        resumen.hallazgos_clave = data.get("hallazgos_clave", "")
        resumen.conclusion_implicaciones = data.get("conclusion_implicaciones", "")

        return resumen

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




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














