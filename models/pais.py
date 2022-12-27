from sqlalchemy import Column, Integer, String

from configs.database import Base

class PaisDB(Base):
    __tablename__ = "pais"

    id = Column(Integer, primary_key=True, index=True)
    codigo = Column(String)
    pais = Column(String)
