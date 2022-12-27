from pydantic import BaseModel, constr
from typing import List, Optional

from datetime import datetime

class AppModel(BaseModel):
    def dict(self, *args, **kwargs):
        if kwargs and kwargs.get("exclude_none") is not None:
            kwargs["exclude_none"] = True
            return BaseModel.dict(self, *args, **kwargs)

class message(AppModel):
    msg: str
    dato: Optional[str]