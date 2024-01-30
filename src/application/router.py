from fastapi import APIRouter, Depends
from sqlalchemy import insert

from sqlalchemy.ext.asyncio import AsyncSession

from src.application.models import application
from src.database import get_async_session
from src.application.schemas import ApplicationCreate


router = APIRouter(
    prefix="/application",
    tags=["Application"],
)


@router.post("/")
async def put_items(new_application: ApplicationCreate, session: AsyncSession = Depends(get_async_session)):
    stmt = insert(application).values(**new_application.model_dump())
    await session.execute(stmt)
    await session.commit()
    # send_email(email, f"Your linkedin account is {linkedin}")
