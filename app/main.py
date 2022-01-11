import sys

import requests
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.routes import estacoes

app = FastAPI(
    title="Backend FastAPI",
    description="FastAPI with frontend HTML using JINJA2",
    default_response_class=ORJSONResponse,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

from loguru import logger

logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | {level} | <level>{message}</level>",
)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")


@app.get("/get_estacoes_inmet")
async def mostrar_estacoes():
    estacoes = requests.get("https://apitempo.inmet.gov.br/estacoes/T")
    return estacoes.json()


@app.get(
    "/mostrar_mapas",
    tags=["Raiz"],
    response_class=HTMLResponse,
    include_in_schema=False,
)
async def mostrar_mapas(request: Request):
    return templates.TemplateResponse("mapas.html", {"request": request})


# MELHORIA (AGRUPAR AS ROTAS QUE EXECUTAM OS MÉTODOS)
app.include_router(estacoes.router)

# 1) Rota Raiz - mostra a página index.html
@app.get("/", tags=["Raiz"], response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
