from sqlalchemy import Column, Integer, String, ForeignKey, BigInteger, DateTime

from configs.database import Base
from models.pais import PaisDB

class PersonaDB(Base):
    __tablename__ = "persona"

    id = Column(BigInteger, primary_key=True, index=True)
    nombre = Column(String)
    telefono = Column(String)
    codigo_postal = Column(String(255))
    pais_nacimiento_id = Column(BigInteger, ForeignKey(f'{PaisDB.__tablename__}.id'))
    deleted = Column(DateTime)
