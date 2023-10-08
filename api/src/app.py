from datetime import datetime, timedelta
from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from config import STATIC_PATH

from database.database import get_session
from database.models import Facility, Group, Teacher
from src.external import get_schedule

from dateutil import parser


app = FastAPI()


@app.get("/view")
async def schedule(type: str,  # schedule, groups, facilities
                   begin: str, end: str,  # 2023-10-07T00:00:00
                   facility_name: str = None,
                   group_name: str = None,
                   teacher_name: str = None,
                   session: AsyncSession = Depends(get_session)):

    if type == "schedule":

        if facility_name != None and all(x == None for x in [teacher_name, group_name]):

            facility_raw = (await session.execute(
                select(Facility.num)
                .filter(Facility.name.ilike('%' + facility_name + '%'))
            )).first()

            if facility_raw == None:
                raise HTTPException(
                    status_code=400, detail="facility not found")

            facility_id = facility_raw._mapping["num"]

            return await get_schedule(facility=facility_id, begin=begin, end=end)

        elif group_name != None and all(x == None for x in [teacher_name, facility_name]):

            group_raw = (await session.execute(
                select(Group.num).where(Group.name == group_name)
            )).first()

            if group_raw == None:
                raise HTTPException(status_code=400, detail="group not found")

            group_id = group_raw._mapping["num"]

            return await get_schedule(group=group_id, begin=begin, end=end)
        
        elif teacher_name != None and all(x == None for x in [group_name, facility_name]):

            teacher_raw = (await session.execute(
                select(Teacher.id).filter(Teacher.name.ilike('%' + teacher_name + '%'))
            )).first()

            if teacher_raw == None:
                raise HTTPException(status_code=400, detail="teacher not found")

            teacher_id = teacher_raw._mapping["id"]

            return await get_schedule(teacher=teacher_id, begin=begin, end=end)

        else:
            raise HTTPException(
                status_code=400, detail="only one param should be used")

    elif type == "groups":

        groups_raw = (await session.execute(
            select(Group.name, Group.num)
        )).all()

        groups = [x._mapping for x in groups_raw]

        return groups

    elif type == "facilities":

        facilities_raw = (await session.execute(
            select(Facility.name, Facility.num)
        )).all()

        facilities = [x._mapping for x in facilities_raw]

        return facilities
    
    elif type == "teachers":

        teachers_raw = (await session.execute(
            select(Teacher.name, Teacher.id)
        )).all()

        teachers = [x._mapping for x in teachers_raw]

        return teachers


@app.get("/check")
async def check_facility(day: datetime,
                         facility_name: str,
                         order: int,
                         session: AsyncSession = Depends(get_session)):

    day_num = day.weekday()

    end = day

    while (day_num < 6):
        day_num += 1
        end = end + timedelta(days=1)

    begin = end - timedelta(days=6)

    if facility_name != None:

        facilities = (await session.execute(
            select(Facility.name).filter(Facility.name.ilike('%' + facility_name + '%'))
        )).all()

    else:

        facilities = (await session.execute(
            select(Facility.name)
        )).all()

    result = []

    for facility_raw in facilities:

        flag = False

        facility = facility_raw._mapping

        events_raw = await schedule("schedule", begin, end,
                                    facility["name"], session=session)

        for event in events_raw:

            if event["order"] == order and \
                parser.parse(event["begin"]).date() == day.date():
                flag = True
                break

        if flag:
            continue

        result.append(facility["name"])

    return result


@app.get("/install_groups")
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


@app.get("/install_teachers")
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


@app.get("/install_facilities")
async def install_classes(session: AsyncSession = Depends(get_session)):

    file = open(f"{STATIC_PATH}/facilities.txt")

    facilities = [(int(x[0].replace('"', '')), x[1].replace('\n', ''))
              for x in [x.split(">") for x in file.readlines()]]

    for facility in facilities:

        facility_insert = {
            "name": facility[1],
            "num": facility[0]
        }

        await session.execute(insert(Facility).values(facility_insert))
        await session.commit()

    return {"detail": "classes install success"}
