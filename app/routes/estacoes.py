from typing import List

import requests
from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.schemas.schemas import Estacao

router = APIRouter(
    prefix="/estacoes",
    tags=["Estações Inmet"],
    responses={404: {"description": "Not found"}},
)
templates = Jinja2Templates(directory="app/templates")


@router.get("/js", tags=["HTML"], response_class=HTMLResponse, include_in_schema=False)
async def page_estacoes_js(request: Request):
    return templates.TemplateResponse("estacoes_js.html", {"request": request})


@router.get("/", response_model=List[Estacao])
async def get_estacoes():
    """Puxa as informações de https://apitempo.inmet.gov.br/estacoes/T"""
    res = requests.get("https://apitempo.inmet.gov.br/estacoes/T")
    return res.json()
