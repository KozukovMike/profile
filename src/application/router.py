from fastapi import APIRouter, Depends
from sqlalchemy import select, insert

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.models import application
from src.database import get_async_session
from src.global_functions import send_email


router = APIRouter(
    prefix="/application",
    tags=["Application"],
)


@router.get("/")
async def put_items(email: str, linkedin: str, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(application).values(email=email, linkedin=linkedin)
    await session.execute(stmt)
    await session.commit()
    send_email(email, f"Your linkedin account is {linkedin}")
