from fastapi import FastAPI, Request
from .database import engine
from .routers import auth, todos, users
from .models import base
from fastapi.templating import Jinja2Templates

app = FastAPI() 

base.metadata.create_all(bind=engine)

templates = Jinja2Templates(directory="todo_app/templates")


@app.get("/")
async def test(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/healthcheck")
async def healthcheck():
    return {"status": "ok"}


app.include_router(auth.router, tags=["auth"], prefix="/auth")
app.include_router(todos.router, tags=["todos"], prefix="/todos")
app.include_router(users.router, tags=["users"], prefix="/users")
