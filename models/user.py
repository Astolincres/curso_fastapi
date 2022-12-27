from sqlalchemy import BigInteger, Column, String
from sqlalchemy.sql import func
from configs.database import Base

class UsersDB(Base):
    __tablename__ = "user"
    id = Column(BigInteger, primary_key=True, index=True)
    password = Column(String(128))
    username = Column(String(150))
