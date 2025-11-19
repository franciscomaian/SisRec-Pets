from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# importa apenas a função main do arquivo api.py
from api import main

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"status": "ok", "msg": "API rodando"}

@app.post("/recomendar/{tipo}")
def recomendar(tipo: str, filtros: dict):

    if tipo == "dog":
        return main("recomendar_dog", criterios=filtros)

    if tipo == "cat":
        return main("recomendar_cat", criterios=filtros)

    return {"status": "erro", "msg": "Tipo inválido"}
