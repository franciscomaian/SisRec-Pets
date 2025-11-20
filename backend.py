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

@app.get("/get/{id}")
def recomendar(id: str):

    if id[0:3] == "dog":
        return main("get_dog", {"id" : id})

    if id[0:3] == "cat":
        return main("get_cat", {"id" : id})

    return {"status": "erro", "msg": "Tipo inválido"}

@app.post("/remover/{id}")
def remover(id: str):
    if id[0:3] == "cat":
        return main("remove_cat", {"id" : id})
    
    if id[0:3] == "dog":
        return main("remove_dog", {"id" : id})
    
    return {"status": "erro", "msg": "Tipo inválido"}

@app.post("/adicionar/")
def adicionar(dados: dict):
    if dados["tipo"] == "cat":
        return main("add_cat", dados)
    
    if dados["tipo"] == "dog":
        return main("add_dog", dados)
    
    return {"status": "erro", "msg": "Tipo inválido"}