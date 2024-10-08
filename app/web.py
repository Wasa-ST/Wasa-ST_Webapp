from dotenv import load_dotenv
import os


from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles

from .routes import router  



app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)
