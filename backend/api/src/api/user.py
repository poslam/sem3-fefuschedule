from database.database import get_session
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

user_router = APIRouter(
    prefix="/user"
)


@user_router.post('/edit')
async def user_edit(group: str,
                    subgroup: str,
                    name: str,
                    session: AsyncSession = Depends(get_session)):  # email?
    pass
