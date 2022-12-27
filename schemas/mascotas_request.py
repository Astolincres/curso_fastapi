from pydantic import BaseModel, constr
from typing import List, Optional

from datetime import datetime

from utils.regex import Regex

class UpdateModel(BaseModel):
    class Config:
        extra = "forbid"

class Patas(UpdateModel):
    numero: Optional[str]
    v1: Optional[str]
    v2: Optional[str]
    v3: str

class CrearMascota(UpdateModel):
    nombre: constr(strict=True, regex=Regex.nombre, max_length=50)
    raza: Optional[constr(strict=True, regex="^[a-zA-Z\sá-ú]+$", max_length=20, min_length=3)]
    edad: constr(strict=True, regex=Regex.digits, max_length=3, min_length=1)
    patas: List[Patas]
    fecha_nacimiento: datetime