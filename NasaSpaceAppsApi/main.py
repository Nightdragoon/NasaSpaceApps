from fastapi import FastAPI
import uvicorn
import sqlalchemy
app = FastAPI()



@app.get("/")
async def root():
    return {"message": "Hello World"}

#para iniciarlo  uvicorn main:app --reload
@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}
