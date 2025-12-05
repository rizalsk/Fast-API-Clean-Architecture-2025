from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
import os

router = APIRouter()

TEMPLATES_DIR = "app/views/welcome"
templates = Jinja2Templates(directory=str(TEMPLATES_DIR))

@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    app_name = os.getenv("APP_NAME", "FastAPI App")
    return templates.TemplateResponse("index.html", {"request": request, "app_name": app_name})
