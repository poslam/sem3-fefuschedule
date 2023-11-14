from datetime import datetime, timedelta

from config import ALGORITHM, AUTH_TOKEN_LIFE, SECRET_AUTH
from database.database import get_session
from database.models import User
from fastapi import APIRouter, Depends, Header, HTTPException
from jwt import decode, encode
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from src.external import get_user_info
from src.utils import time

auth_router = APIRouter(
    prefix="/auth"
)


async def type_required(types: list, auth: str = Header(None),
                        session: AsyncSession = Depends(get_session)):
    data = None
    try:
        data = decode(auth, SECRET_AUTH, algorithms=[ALGORITHM])

        token_expired_time = datetime.strptime(
            data["expired"], "%Y-%m-%d %H:%M:%S.%f")

        if token_expired_time < time():
            raise Exception

    except:
        raise HTTPException(status_code=401, detail="token is invalid")

    user = await session.get(User, data["id"])

    if user == None:
        raise HTTPException(status_code=400, detail="user not found")

    if types != []:
        if user.type.name not in types and user.type.name != "superadmin":
            raise HTTPException(status_code=403, detail="not allowed")

    return user


async def login_required(auth: str = Header(None),
                         session: AsyncSession = Depends(get_session)):
    return await type_required([], auth, session)


async def student_required(auth: str = Header(None),
                           session: AsyncSession = Depends(get_session)):
    return await type_required(["student"], auth, session)


async def teacher_required(auth: str = Header(None),
                           session: AsyncSession = Depends(get_session)):
    return await type_required(["teacher"], auth, session)


async def elder_required(auth: str = Header(None),
                         session: AsyncSession = Depends(get_session)):
    return await type_required(["elder"], auth, session)


async def moderator_required(auth: str = Header(None),
                             session: AsyncSession = Depends(get_session)):
    return await type_required(["moderator"], auth, session)


def make_token(user_id: int):
    return encode(
        {"id": user_id, "expired": str(
            time() + timedelta(days=int(AUTH_TOKEN_LIFE)))},
        SECRET_AUTH,
    )


@auth_router.get("/login")
async def login_func(ya_token: str,
                     session: AsyncSession = Depends(get_session)):

    user_info = await get_user_info(ya_token)

    name = user_info["display_name"]
    email = user_info["default_email"]

    if any(x not in email for x in ['@students.dvfu.ru', '@dvfu.ru']):
        raise HTTPException(status_code=400, detail='not fefu account')

    user_raw = (await session.execute(
        select(User).where(User.email == email)
    )).first()

    user_insert = {
        "name": name,
        "email": email
    }

    if user_raw == None:

        await session.execute(
            insert(User).values(user_insert)
        )
        await session.commit()

        user_raw = (await session.execute(
            select(User).where(User.email == email)
        )).first()

    user = user_raw[0]

    return {"token": make_token(user["id"]),
            "type": user["type"].name,
            "group": user["group"],
            "subgroup": user["subgroup"],
            "theme": user["theme"],
            "color": user["color"]}
