from urllib import request

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi_users import fastapi_users, FastAPIUsers

from autintification.database import User
from autintification.main_auth import auth_backend
from autintification.manager import get_user_manager
from autintification.schemas import UserRead, UserCreate

templates = Jinja2Templates(directory='static/tamplates')
app = FastAPI()


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

current_user = fastapi_users.current_user()


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"


app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/hello/{name}")
async def say_hello(name: str, request: Request):
    return templates.TemplateResponse("123.html", {"request": request})


@app.get('/')
async def welcome_page(request: Request):
    return templates.TemplateResponse("check.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000,  reload=True)
