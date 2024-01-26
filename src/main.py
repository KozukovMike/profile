import httpx
from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi_users import FastAPIUsers

from src.autintification.models import User
from src.autintification.base_config import auth_backend
from src.autintification.manager import get_user_manager
from src.autintification.schemas import UserRead, UserCreate
from src.application.router import router as router_application

app = FastAPI()
templates = Jinja2Templates(directory="../static/templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")


fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)

app.include_router(router_application)

current_user = fastapi_users.current_user()


@app.post("/sign_in")
async def sign_in(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    data = {
        "email": "string111",
        "password": "string111",
        "username": "string111",
        "role_id": 0
    }
    async with httpx.AsyncClient() as client:
        response = await client.post("http://127.0.0.1:8000/auth/register", json=data)
        response_data = response.json()

    return {"message": "Пользователь успешно зарегистрирован", "response": response_data}


@app.post("/login")
async def login(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
    data = {
        "password": "18",
        "username": "17",
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            'http://127.0.0.1:8000/auth/jwt/login',
            json=data
        )
        response_data = response.json()

    return {"message": "Пользователь успешно вошел", "response": response_data}


@app.get("/hello/{name}")
async def say_hello(name: str, request: Request):
    return templates.TemplateResponse("123.html", {"request": request})


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("check.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000,  reload=True)
