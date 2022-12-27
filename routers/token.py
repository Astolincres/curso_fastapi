from fastapi import APIRouter, Depends
from services.token import TokenService
from schemas.token import Token
from schemas.user import Credential
from fastapi.security import OAuth2PasswordRequestForm

from utils.service_result import handle_result

from configs.database import get_db

router = APIRouter(
    prefix="/tokens",
    tags=["General"],
    responses={404: {"description": "Not found"}},
)

@router.post("", response_model=Token, summary="Solicitar token")
async def open_api_token(form_data: OAuth2PasswordRequestForm = Depends(), db: get_db = Depends()):
    user = Credential(username = form_data.username, password = form_data.password)
    result = TokenService(db).create_token(user)
    return handle_result(result)
