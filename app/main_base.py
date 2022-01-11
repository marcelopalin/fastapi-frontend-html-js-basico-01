import os
from datetime import datetime
from typing import List

from dynaconf import Dynaconf
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, ORJSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sh import tail
from sse_starlette.sse import EventSourceResponse

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=["settings.toml", ".secrets.toml"],
    environments=True,
    load_dotenv=True,
    dotenv_path="app/.env",
)

import random
import time

from fastapi.websockets import WebSocket

from app.routes import estacoes, users
from app.routes.files import download, upload
from app.routes.geocode_routes import geoforward, georeverse

app = FastAPI(
    title=settings.APP_NAME,
    description=settings.APP_DESCRIPTION,
    version=settings.APP_VERSAO,
    default_response_class=ORJSONResponse,
    debug=True,
)


origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5000",
    "http://localhost:8000",
    "http://localhost:8081",
    "http://localhost:8082",
]

app.add_middleware(
    CORSMiddleware,
    # allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

real_path = os.path.realpath(__file__)
dir_path = os.path.dirname(real_path)
LOGFILE = f"{dir_path}/test.log"

# This async generator will listen to our log file in an infinite while loop (happens in the tail command)
# Anytime the generator detects a new line in the log file, it will yield it.
async def logGenerator(request):
    for line in tail("-f", LOGFILE, _iter=True):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield line
        time.sleep(0.5)


app.include_router(estacoes.router)
app.include_router(upload.router)
app.include_router(download.router)


# Redireciona para documentação
# @app.get("/", name="Home Page", description="API Documentation Page.", include_in_schema=False)
# async def main():
#     """API Documentation Page."""
#     return RedirectResponse(url="/docs/")

# include_in_schema=False oculta a rota da documentação
@app.get("/", tags=["HTML"], response_class=HTMLResponse, include_in_schema=False)
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Rota do Html
@app.get("/sse", tags=["HTML"], response_class=HTMLResponse, include_in_schema=False)
async def sse_server_side_event(request: Request):
    return templates.TemplateResponse("sse.html", {"request": request})


# This async generator will listen to our log file in an infinite while loop (happens in the tail command)
# Anytime the generator detects a new line in the log file, it will yield it.
async def logGenerator(request):
    for line in tail("-f", LOGFILE, _iter=True):
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield line
        time.sleep(0.5)


async def generate_log_msgs(request):
    status_stream_delay = 5  # second
    status_stream_retry_timeout = 30000  # milisecond
    count = 0
    while True:
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield f"Executando comparador {count}"
        count += 1
        time.sleep(0.5)

        if count == 2:
            yield {
                "event": "update",
                "retry": status_stream_retry_timeout,
                "data": "Atualizado!",
            }

        if count == 10:
            yield {"event": "end", "data": ""}
            break


# This is our api endpoint. When a client subscribes to this endpoint, they will recieve SSE from our log file
@app.get("/comparador-stream-logs")
async def run_comparador(request: Request):
    # event_generator = logGenerator(request)
    event_generator = generate_log_msgs(request)
    return EventSourceResponse(event_generator)


# # Rota do Html
# @app.get(
#     "/websockets_js", tags=["HTML"], response_class=HTMLResponse, include_in_schema=False
# )
# async def websocket(request: Request):
#     return templates.TemplateResponse("websocket.html", {"request": request})

# # Rota do Websocket Html com Vue
# @app.get(
#     "/websockets_vue", tags=["HTML"], response_class=HTMLResponse, include_in_schema=False
# )
# async def websocket_vue(request: Request):
#     return templates.TemplateResponse("websocket_vue.html", {"request": request})

# Tunel 1 de conexao Socket
@app.websocket("/comparador_ws")
async def websocket_endpoint(websocket: WebSocket):
    print("Esperando conexão...")
    await websocket.accept()
    while True:
        # So continua quando o cliente enviar Msg! Fica Esperando!
        data = await websocket.receive_text()
        print(f"SERVER: a msg vinda do cliente = {data}")
        await websocket.send_text(f"RETORNANDO: {data}")
        await websocket.send_json({"modelo": "CFSv2", "ID": "1", "Acao": "Comparar"})


@app.get(
    "/estacoes_js", tags=["HTML"], response_class=HTMLResponse, include_in_schema=False
)
async def page2(request: Request):
    return templates.TemplateResponse("estacoes_js.html", {"request": request})


# Rota Raíz - Página Principal
app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")
