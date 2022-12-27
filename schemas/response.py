from pydantic import BaseModel
from typing import Optional


class AppModel(BaseModel):
    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
            return BaseModel.dict(self, *args, **kwargs)

class Message(AppModel):
    msg: str

class PersonaR(AppModel):
    nombre : str
    telefono : str
    codigo_postal : str
    pais_nacimiento : Optional[str]