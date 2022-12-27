from fastapi import APIRouter, Depends

from typing import List

from utils.service_result import handle_result

from configs.database import get_db

from schemas.mascotas_request import CrearMascota
from schemas.mascotas_response import message

router = APIRouter(
    prefix="/mascotas",
    tags=["Mascotas CRUD"],
    responses={404: {"description": "Not found"}},
)

@router.post("/C", summary="Crear mascotas", response_model=message)
async def crear_mascotas(item: CrearMascota, db: get_db = Depends()):
    print(item)
    #result = PersonasService(db).crear_persona(item)
    return {'msg': 'Creado', 'dato': None}

@router.get('/{id}')
async def get_mascotas(id: int):
    return id