from config import STATIC_PATH
from database.models import Facility, Group, Teacher
from fastapi import APIRouter, Depends
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session

install_router = APIRouter(
    prefix="/install"
)


@install_router.get("/groups")
async def install_groups(session: AsyncSession = Depends(get_session)):

    file = open(f"{STATIC_PATH}/groups.txt")

    groups = [(int(x[0].replace('"', '')), x[1].replace('\n', ''))
              for x in [x.split(">") for x in file.readlines()]]

    for group in groups:

        group_insert = {
            "name": group[1],
            "num": group[0]
        }

        await session.execute(insert(Group).values(group_insert))
        await session.commit()

    return {"detail": "groups install success"}


@install_router.get("/teachers")
async def install_gropus(session: AsyncSession = Depends(get_session)):

    file = open(f"{STATIC_PATH}/teachers.txt")

    teachers = [(x[0].replace('"', ''), x[1].replace('\n', ''))
                for x in [x.split(">") for x in file.readlines()]]

    for teacher in teachers:

        teacher_insert = {
            "name": teacher[1],
            "id": teacher[0]
        }

        await session.execute(insert(Teacher).values(teacher_insert))
        await session.commit()

    return {"detail": "teachers install success"}


@install_router.get("/facilities")
async def install_classes(session: AsyncSession = Depends(get_session)):

    file = open(f"{STATIC_PATH}/facilities.txt")

    facilities = [(int(x[0].replace('"', '')), x[1].replace('\n', ''))
                  for x in [x.split(">") for x in file.readlines()]]

    for facility in facilities:

        facility_insert = {
            "name": facility[1],
            "num": facility[0],
            "spec": "unknown"
        }

        await session.execute(insert(Facility).values(facility_insert))
        await session.commit()

    return {"detail": "facilities install success"}
