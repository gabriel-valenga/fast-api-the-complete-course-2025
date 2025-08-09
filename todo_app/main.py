from fastapi import FastAPI
from database import engine
from routers import admin, auth, todos, users
import models

app = FastAPI() 

models.base.metadata.create_all(bind=engine)

app.include_router(auth.router, tags=["auth"])
app.include_router(todos.router, tags=["todos"])
app.include_router(users.router, tags=["users"])
