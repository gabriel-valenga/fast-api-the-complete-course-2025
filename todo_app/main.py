from typing import Annotated
from fastapi import FastAPI, Depends
from database import engine, session_local
from sqlalchemy.orm import Session
import models

app = FastAPI() 

models.base.metadata.create_all(bind=engine)

def get_db():
    db = session_local()
    try:
        yield db
    finally:
        db.close()


db_dependency = Annotated[Session, Depends(get_db)]


@app.get("/")
def read_all_todos(db: db_dependency):
    todos = db.query(models.Todos).all()
    return {"todos": todos}
