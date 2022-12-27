from sqlalchemy import BigInteger, Column, String, Boolean, DateTime, Integer
from sqlalchemy.sql import func
from configs.database import Base

from utils.enums import typeHistorial

class TokenDB(Base):
    __tablename__ = "cs_token"
    id = Column(BigInteger, primary_key=True, index=True)
    user_id = Column(Integer, nullable=True)
    token = Column(String(255), nullable=True)

    deleted = Column(DateTime, default=None)
    deleted_by_cascade = Column(Boolean, default=False)
    created_by_id = Column(BigInteger,default=1)
    created_at = Column(DateTime, default=func.now())

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)

class Historical_TokenDB(Base):
    __tablename__ = 'catalogos_modular_historicaltoken'

    history_id = Column(BigInteger, primary_key=True, index=True)
    history_date = Column(DateTime, default=func.now())
    history_change_reason = Column(String, default=None)
    history_type = Column(String, default=typeHistorial.ADD.value)
    history_user_id = Column(BigInteger)

    id = Column(BigInteger)
    user_id = Column(Integer, nullable=True)
    token = Column(String(255), nullable=True)

    deleted = Column(DateTime, default=None)
    deleted_by_cascade = Column(Boolean, default=False)
    created_by_id = Column(BigInteger,default=1)
    created_at = Column(DateTime, default=func.now())

    def __init__(self, *args, **kwargs):
        return super().__init__(*args, **kwargs)