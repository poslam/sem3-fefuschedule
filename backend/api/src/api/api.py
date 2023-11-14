from datetime import datetime, timedelta

from database.database import get_session
from database.models import Event, Facility, Group, Subgroup, Teacher
from dateutil import parser
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.auth import auth_router, login_required, shared
from src.api.event import event_router
from src.api.install import install_router
from src.api.user import user_router
from src.utils import event_filter, event_updater, facility_spec_parser

api_router = APIRouter(
    prefix="/api"
)

api_router.include_router(install_router)
api_router.include_router(auth_router)
api_router.include_router(event_router)
api_router.include_router(user_router)


@api_router.get("/serverStatus")
async def test(back: BackgroundTasks,
               session: AsyncSession = Depends(get_session)):
    try:

        back.add_task(event_updater, session)

        await session.execute(select(Facility))
        return {"detail": "server and database are working!"}
    except BaseException:
        return {"detail": "connection to the database is corrupted"}


@api_router.get('/view')
async def view_structure(type: str,  # groups, facilities, teachers
                         user=Depends(login_required),
                         session: AsyncSession = Depends(get_session)):

    if type == "groups":

        groups_raw = (await session.execute(
            select(Group.name, Group.num)
        )).all()

        result = []

        for group_raw in groups_raw:

            group = group_raw._mapping

            subgroups = [x._mapping["name"] for x in (await session.execute(
                select(Subgroup.name).where(Subgroup.group == group["name"])
            )).all()]

            result.append({"group": group["name"],
                           "subgroups": subgroups})

        return result

    elif type == "facilities":

        facilities_raw = (await session.execute(
            select(Facility.name, Facility.num,
                   Facility.spec, Facility.capacity)
        )).all()

        facilities = [facility_spec_parser(x._mapping) for x in facilities_raw]

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
async def check_facility(day: str,
                         facility_name: str,
                         order: int,
                         spec: str = None,  # lecture, lab_or_prac
                         user=Depends(shared),
                         session: AsyncSession = Depends(get_session)):
    try:
        day: datetime = parser.parse(day)
    except:
        raise HTTPException(status_code=400, detail="incorrect parameter: day")

    begin = day
    end = day + timedelta(days=1)

    if spec == None:

        if facility_name is not None:

            facilities = (await session.execute(
                select(Facility.name, Facility.spec, Facility.capacity).filter(
                    Facility.name.ilike('%' + facility_name + '%'))
            )).all()

        else:

            facilities = (await session.execute(
                select(Facility.name, Facility.spec, Facility.capacity)
            )).all()

    else:

        if facility_name is not None:

            facilities = (await session.execute(
                select(Facility.name, Facility.spec, Facility.capacity)
                .filter(Facility.name.ilike('%' + facility_name + '%'))
                .where(Facility.spec == spec)
            )).all()

        else:

            facilities = (await session.execute(
                select(Facility.name, Facility.spec, Facility.capacity)
                .where(Facility.spec == spec)
            )).all()

    result = []

    for facility_raw in facilities:

        facility = facility_raw._mapping

        events = [x._mapping for x in (await session.execute(
            select(Event)
            .where(Event.facility == facility["name"])
            .where(Event.order == order)
            .where(Event.begin >= begin)
            .where(Event.end <= end)
        )).all()]

        if events == []:
            result.append({"name": facility["name"],
                           "spec": facility["spec"],
                           "capacity": facility["capacity"]})

    return result
