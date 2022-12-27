from typing import List
from fastapi import APIRouter, Depends
from utils.auth import get_current_user
from schemas.user import UserData
from services.user import UserService
from utils.service_result import handle_result
from schemas.user import User, UserCreate

from configs.database import get_db

router = APIRouter(
    prefix="/users",
    tags=["Users"],
    responses={404: {"description": "Not found"}},
)

@router.get("/{id}", response_model = User, summary = "Devuelve un objeto de tipo User con el id indicado en el parametro, devuelve un error si no existe")
async def get_user(id: int, db: get_db = Depends(), user: User = Depends(get_current_user)):
    result = UserService(db).get_user(id)
    return handle_result(result)

@router.get("/username/{username}", response_model = User, summary = "Devuelve un objeto de tipo User con el Username indicado en el parametro, devuelve un error si no existe")
async def get_user_by_username(username: str, db: get_db = Depends(), user: User = Depends(get_current_user)):
    print(username)
    result = UserService(db).get_user_by_username(username)
    return handle_result(result)

@router.get("/", response_model = List[User], summary = "Devuelve todos los objetos de tipo User, devuelve un arreglo vacio si no existen")
async def get_all(db: get_db = Depends(), user: User = Depends(get_current_user)):
    result = UserService(db).get_all()
    return handle_result(result)

@router.post("/", response_model = User, status_code = 201, summary = "Crea un objeto de tipo User con los datos enviados en el body, devuelve un error si ya existe")
async def create_user(user_request: UserCreate, db: get_db = Depends(), user: User = Depends(get_current_user)):
    result = UserService(db).create_user(user_request)
    return handle_result(result)

@router.put("/{id}", response_model = User, status_code = 200, summary = "Actualiza un objeto de tipo User con los datos enviados en el body, devuelve un error si no existe")
async def update_user(id: int, user_request:UserCreate, db: get_db = Depends(), user: User = Depends(get_current_user)):
    result = UserService(db).update_user(id, user_request)
    return handle_result(result)

@router.delete("/{id}", response_model = User, summary="Elimina un objeto de tipo User con el id indicado en el parametro, devuelve un error si no existe")
async def delete_user(id: int, user_request:UserData, db: get_db = Depends(), user: User = Depends(get_current_user)):
    result = UserService(db).delete_user(user_request)
    return handle_result(result)
