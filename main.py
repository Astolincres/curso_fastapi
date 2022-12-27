from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.security import OAuth2PasswordBearer

from routers import token, persona, mascotas

from configs.database import create_tables

from starlette.exceptions import HTTPException as StarletteHTTPException

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from utils.app_exceptions import AppExceptionCase
from utils.request_exceptions import (
    http_exception_handler,
    request_validation_exception_handler,
)
from utils.app_exceptions import app_exception_handler

# Es el ORM que te genera todas las tablas declaradas en el modelo
create_tables()

limiter = Limiter(key_func=get_remote_address)

tags_metadata = [
    {
        "name": "General",
        "description": "Obtener token."
    },
    {
        "name": "Personas CRUD",
        "description": "CRUD de personas"
    },
    {
        "name": "Mascotas CRUD",
        "description": "CRUD de mascotas"
    }
]

dec = """
## _**Hola**_
"""

app = FastAPI(
    title="FastAPI-Template",
    description=dec,
    version="1.0.0",
    openapi_url="/api/v1/openapi.json",
    openapi_tags=tags_metadata
)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request, e):
    return await http_exception_handler(request, e)

@app.exception_handler(RequestValidationError)
async def custom_validation_exception_handler(request, e):
    return await request_validation_exception_handler(request, e)

@app.exception_handler(AppExceptionCase)
async def custom_app_exception_handler(request, e):
    return await app_exception_handler(request, e)

app.include_router(token.router)
app.include_router(persona.router)
app.include_router(mascotas.router)