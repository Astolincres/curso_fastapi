from pydantic import BaseModel, constr
from typing import List, Optional

from datetime import datetime

from utils.regex import Regex

digitos = "^\d+$"

class UpdateModel(BaseModel):
    class Config:
        extra = "forbid"

class Hijos(UpdateModel):
    edad: int

class Persona(UpdateModel):
    edad: int
    nombre: constr(strict=True, regex=Regex.nombre)
    telefono: Optional[constr(strict=True, regex=digitos, max_length=10)]
    codigo_postal: constr(strict=True, regex=digitos, max_length=5)
    pais_nacimiento: str
    fecha_nacimiento: datetime
    hijos: Optional[List[Hijos]]