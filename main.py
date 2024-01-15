from urllib import request

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn


templates = Jinja2Templates(directory='static/tamplates')
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/hello/{name}")
async def say_hello(name: str, request: Request):
    return templates.TemplateResponse("123.html", {"request": request})


@app.get('/')
async def welcome_page(request: Request):
    return templates.TemplateResponse("check.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000,  reload=True)
