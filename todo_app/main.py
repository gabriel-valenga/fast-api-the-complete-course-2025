from fastapi import FastAPI
from database import engine
from routers import admin, auth, todos
import models

app = FastAPI() 

models.base.metadata.create_all(bind=engine)

app.include_router(auth.router, tags=["auth"])
app.include_router(todos.router, tags=["todos"])

