from fastapi import APIRouter


router = APIRouter(
    prefix="/admin",
    tags=["Admin"],
)

@router.get("/")
async def root():
    return {"message": "Hello World"}
