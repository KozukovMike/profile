from fastapi import APIRouter, Depends
from sqlalchemy import select

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.models import application
from src.database import get_async_session

router = APIRouter(
    prefix="/application",
    tags=["Application"],
)


@router.get("/")
async def root(email: str, session: AsyncSession = Depends(get_async_session)):
    query = select(application).where(application.c.email == email)
    result = await session.execute(query)
    session.commit()
    return result.all()
