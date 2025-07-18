from database import base
from sqlalchemy import Column, Integer, String, Boolean

class Todos(base):
    __tablename__ = "todos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, nullable=True)
    priority = Column(Integer, default=1)
    completed = Column(Boolean, default=False)