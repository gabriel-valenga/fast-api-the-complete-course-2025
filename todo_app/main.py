from fastapi import FastAPI
from database import engine
import models

app = FastAPI() 

models.base.metadata.create_all(bind=engine)