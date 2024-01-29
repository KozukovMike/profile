from typing import Annotated

import httpx
from fastapi import FastAPI, Request, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import uvicorn
from fastapi_users import FastAPIUsers
from fastapi.responses import RedirectResponse

from src.autintification.models import User
from src.autintification.base_config import auth_backend, fastapi_users
from src.autintification.schemas import UserRead, UserCreate
from src.application.router import router as router_application

app = FastAPI()
templates = Jinja2Templates(directory="../static/templates")
app.mount("/static", StaticFiles(directory="../static"), name="static")


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



# @app.post("/sign_in")
# async def sign_in(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
#     data = {
#         "email": "string111",
#         "password": "string111",
#         "username": "string111",
#         "role_id": 0
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.post("http://127.0.0.1:8000/auth/register", json=data)
#         response_data = response.json()
#
#     return {"message": "Пользователь успешно зарегистрирован", "response": response_data}
#
#
# @app.post("/login")
# async def login(username: str = Form(...), email: str = Form(...), password: str = Form(...)):
#     data = {
#         "password": "18",
#         "username": "17",
#     }
#     async with httpx.AsyncClient() as client:
#         response = await client.post(
#             'http://127.0.0.1:8000/auth/jwt/login',
#             json=data
#         )
#         response_data = response.json()
#
#     return {"message": "Пользователь успешно вошел", "response": response_data}
@app.post("/sign_in")
async def sign_in(
                request: Request,
                username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                email: Annotated[str, Form()]
                ):

    data = {
        "email": email,
        "password": password,
        "username": username,
        "role_id": 1
    }
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f'{request.base_url}auth/register',
            json=data,
        )

    if response.status_code in [200, 201, 204]:
        redirect = RedirectResponse(url=f'{request.base_url}hello/world', status_code=status.HTTP_302_FOUND)
        redirect.set_cookie(key='auth', value=response.cookies.get('auth'), httponly=True)

        return redirect


@app.post("/login")
async def login(
                request: Request,
                username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                email: Annotated[str, Form()]
                ):
    data = {
        "password": password,
        "username": email,
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(
            url=f'{request.base_url}auth/jwt/login',
            headers={
                'accept': 'application/json',
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            data=data,
        )

    # response_data = response.json()

    # return {"message": "Пользователь успешно вошел", "response": response_data}

    if response.status_code in [200, 201, 204]:
        cookies = response.cookies['fastapiusers']
        redirect = RedirectResponse(url=f'{request.base_url}hello/world', status_code=status.HTTP_302_FOUND)
        print(cookies)
        # for cookie in cookies:
        redirect.set_cookie(key='fastapiusers', value=cookies, httponly=True)

        return redirect


@app.post("/logout")
async def logout(
                request: Request,
                username: Annotated[str, Form()],
                password: Annotated[str, Form()],
                email: Annotated[str, Form()]
                ):
    async with httpx.AsyncClient() as client:
        await client.post(
            url=f'{request.base_url}auth/jwt/logout',
            headers={
                'accept': 'application/json',
            },
            cookies={'fastapiusers': request.cookies.get('fastapiusers')}
        )

    # response_data = response.json()

    # return {"message": "Пользователь успешно вошел", "response": response_data}

    redirect_response = RedirectResponse(url=f'{request.base_url}hello/world', status_code=status.HTTP_302_FOUND)
    redirect_response.delete_cookie('fastapiusers')

    return redirect_response


@app.get("/hello/{name}")
async def say_hello(name: str, request: Request):
    return {"akckl": name, "request": request.base_url}


@app.get("/")
async def root(request: Request):
    return templates.TemplateResponse("check.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run(app='main:app', host='127.0.0.1', port=8000,  reload=True)
