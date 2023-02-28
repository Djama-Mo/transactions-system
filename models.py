from database import Base
from sqlalchemy import String, Integer, Column


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    cash = Column(Integer, nullable=False, default=0)
