from fastapi import APIRouter, Request
from starlette.templating import Jinja2Templates


templates = Jinja2Templates(directory="../static/templates")

router = APIRouter(
    prefix="/cv",
    tags=["CV"],
)


@router.get("/")
async def root(request: Request):
    return templates.TemplateResponse("cv.html", {"request": request, "base_url": request.base_url})
