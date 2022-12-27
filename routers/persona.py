from fastapi import APIRouter, Depends

from utils.service_result import handle_result

from configs.database import get_db

from schemas.persona import Persona
from schemas.response import Message, PersonaR

from services.personas import PersonasService

router = APIRouter(
    prefix="/persona",
    tags=["Personas CRUD"],
    responses={404: {"description": "Not found"}},
)

@router.post("/C", summary="Crear persona", response_model=Message)
async def crear_persona(item: Persona, db: get_db = Depends()):
    result = PersonasService(db).crear_persona(item)
    return handle_result(result)

@router.get("/R/{id}", summary="Leer persona", response_model=PersonaR)
async def crear_persona(id:int, db: get_db = Depends()):
    result = PersonasService(db).get_persona(id)
    return handle_result(result)

@router.put("/P/{id}", summary="Leer persona")
async def crear_persona(id:int, item: Persona, db: get_db = Depends()):
    result = PersonasService(db).actualizar(id, item)
    return handle_result(result)

@router.delete('/D/{id}', summary="Eliminar persona")
async def crear_persona(id:int, db: get_db = Depends()):
    result = PersonasService(db).eliminar(id)
    return handle_result(result)