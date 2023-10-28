from datetime import datetime, timedelta

from database.models import Facility, Group, Teacher
from dateutil import parser
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.install import install_router
from src.external import get_schedule

from database.database import get_session

api_router = APIRouter(
    prefix="/api"
)

api_router.include_router(install_router)


@api_router.get("/serverStatus")
async def test(session: AsyncSession = Depends(get_session)):
    try:
        await session.execute(select(Facility))
        return {"detail": "server and database are working!"}
    except:
        return {"detail": "connection to the database is corrupted"}


@api_router.get("/view")
async def schedule(begin: str, end: str,  # 2023-10-07T00:00:00
                   facility_name: str = None,
                   group_name: str = None,
                   teacher_name: str = None,
                   session: AsyncSession = Depends(get_session)):

    if facility_name != None and all(x == None for x in [teacher_name, group_name]):

        facility_raw = (await session.execute(
            select(Facility.num)
            .filter(Facility.name.ilike('%' + facility_name + '%'))
        )).first()

        if facility_raw == None:
            raise HTTPException(
                status_code=400, detail="facility not found")

        facility_id = facility_raw._mapping["num"]

        temp = await get_schedule(facility=facility_id, begin=begin, end=end)

        events = temp["events"]

    elif group_name != None and all(x == None for x in [teacher_name, facility_name]):

        group_raw = (await session.execute(
            select(Group.num).where(Group.name == group_name)
        )).first()

        if group_raw == None:
            raise HTTPException(status_code=400, detail="group not found")

        group_id = group_raw._mapping["num"]

        temp = await get_schedule(group=group_id, begin=begin, end=end)

        events = temp["events"]

        await session.execute(
            update(Group).where(Group.num == group_id).values(
                subgroups_count=temp["subgroups"])
        )
        await session.commit()

    elif teacher_name != None and all(x == None for x in [group_name, facility_name]):

        teacher_raw = (await session.execute(
            select(Teacher.id).filter(
                Teacher.name.ilike('%' + teacher_name + '%'))
        )).first()

        if teacher_raw == None:
            raise HTTPException(status_code=400, detail="teacher not found")

        teacher_id = teacher_raw._mapping["id"]

        temp = await get_schedule(teacher=teacher_id, begin=begin, end=end)

        events = temp["events"]

    else:
        raise HTTPException(
            status_code=400, detail="only one param should be used")

    return events


@api_router.get('/view_structure')
async def view_structure(type: str,  # groups, facilities, teachers
                         session: AsyncSession = Depends(get_session)):

    if type == "groups":

        groups_raw = (await session.execute(
            select(Group.name, Group.num, Group.subgroups_count)
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

    else:
        raise HTTPException(status_code=400, detail="incorrect type")


@api_router.get("/check")
async def check_facility(day: datetime,
                         facility_name: str,
                         order: int,
                         session: AsyncSession = Depends(get_session)):

    begin = day
    end = day + timedelta(days=1)

    if facility_name != None:

        facilities = (await session.execute(
            select(Facility.name).filter(
                Facility.name.ilike('%' + facility_name + '%'))
        )).all()

    else:

        facilities = (await session.execute(
            select(Facility.name)
        )).all()

    result = []

    for facility_raw in facilities:

        flag = False

        facility = facility_raw._mapping

        events_raw = await schedule(begin, end,
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


@api_router.get("/event_update")
async def event_updater(session: AsyncSession = Depends(get_session)):

    day = datetime.utcnow()

    day_num = day.weekday()

    end = day

    while (day_num < 6):
        day_num += 1
        end = end + timedelta(days=1)

    begin = end - timedelta(days=6)

    groups = (await session.execute(
        select(Group.name, Group.num)
    )).all()

    for group_raw in groups:
        group = group_raw._mapping

        events = (await get_schedule(group=group["num"], begin=begin, end=end))["events"]


