from fastapi import FastAPI
from database import engine
from routers import auth, todos, users
import models

app = FastAPI() 

models.base.metadata.create_all(bind=engine)


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


app.include_router(auth.router, tags=["auth"], prefix="/auth")
app.include_router(todos.router, tags=["todos"], prefix="/todos")
app.include_router(users.router, tags=["users"], prefix="/users")
