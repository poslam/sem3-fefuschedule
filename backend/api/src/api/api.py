from datetime import datetime, timedelta

from dateutil import parser
from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from database.models import Event, Facility, Group, Teacher
from src.api.install import install_router
from src.utils import event_updater, facility_spec_parser

api_router = APIRouter(
    prefix="/api"
)

api_router.include_router(install_router)


@api_router.get("/serverStatus")
async def test(back: BackgroundTasks,
               session: AsyncSession = Depends(get_session)):
    try:

        back.add_task(event_updater, session)

        await session.execute(select(Facility))
        return {"detail": "server and database are working!"}
    except BaseException:
        return {"detail": "connection to the database is corrupted"}


@api_router.get("/view")
async def schedule(begin: str, end: str,  # 2023-10-07T00:00:00
                   facility_name: str = None,
                   group_name: str = None,
                   teacher_name: str = None,
                   subgroup: str = None,  # 3 or 3,4,5
                   session: AsyncSession = Depends(get_session)):

    begin = parser.parse(begin)
    end = parser.parse(end)

    if facility_name is not None and all(
            x is None for x in [teacher_name, group_name]):

        facility_raw = (await session.execute(
            select(Facility.name, Facility.capacity)
            .filter(Facility.name.ilike('%' + facility_name + '%'))
        )).first()

        if facility_raw is None:
            raise HTTPException(
                status_code=400, detail="facility not found")

        facility = facility_raw._mapping["name"]

        events_raw = (await session.execute(
            select(Event.id.label("event_id"),
                   Event.name.label("event_name"),
                   Event.order,
                   Event.begin,
                   Event.end,
                   Event.facility,
                   Facility.spec,
                   Event.capacity,
                   Event.teacher,
                   Event.group,
                   Event.subgroup)
            .where(Event.facility == facility)
            .where(Facility.name == Event.facility)
            .where(Event.begin >= begin)
            .where(Event.end <= end)
        )).all()
        
        events = []
        
        for event_raw in events_raw:
            
            event = event_raw._mapping
            
            event["capacity"] = facility_raw._mapping["capacity"]
            
            event = facility_spec_parser(event)
            
            events.append(event)
            

    elif group_name is not None and all(x is None for x in [teacher_name, facility_name]):

        group_raw = (await session.execute(
            select(Group.name).where(Group.name == group_name)
        )).first()

        if group_raw is None:
            raise HTTPException(status_code=400, detail="group not found")

        group = group_raw._mapping["name"]

        events_raw = (await session.execute(
            select(Event.id.label("event_id"),
                   Event.name.label("event_name"),
                   Event.order,
                   Event.begin,
                   Event.end,
                   Event.facility,
                   Facility.spec,
                   Event.capacity,
                   Event.teacher,
                   Event.group,
                   Event.subgroup)
            .where(Event.group == group)
            .where(Facility.name == Event.facility)
            .where(Event.begin >= begin)
            .where(Event.end <= end)
        )).all()
        
        events = []
        
        for event_raw in events_raw:
            
            event = event_raw._mapping
            
            facility_raw = (await session.execute(
                select(Facility.capacity).where(Facility.name == event["facility"])
            )).first()
            
            if facility_raw != None:
                event["capacity"] = facility_raw._mapping["capacity"]
            
            event = facility_spec_parser(event)
            
            events.append(event)

    elif teacher_name is not None and all(x is None for x in [group_name, facility_name]):

        teacher_raw = (await session.execute(
            select(Teacher.name).filter(
                Teacher.name.ilike('%' + teacher_name + '%'))
        )).first()

        if teacher_raw is None:
            raise HTTPException(status_code=400, detail="teacher not found")

        teacher = teacher_raw._mapping["name"]
        
        events_raw = (await session.execute(
            select(Event.id.label("event_id"),
                   Event.name.label("event_name"),
                   Event.order,
                   Event.begin,
                   Event.end,
                   Event.facility,
                   Facility.spec,
                   Event.capacity,
                   Event.teacher,
                   Event.group,
                   Event.subgroup)
            .where(Event.teacher == teacher)
            .where(Facility.name == Event.facility)
            .where(Event.begin >= begin)
            .where(Event.end <= end)
        )).all()
        
        events = []
        
        for event_raw in events_raw:
            
            event = event_raw._mapping
            
            facility_raw = (await session.execute(
                select(Facility.capacity).where(Facility.name == event["facility"])
            )).first()
            
            if facility_raw != None:
                event["capacity"] = facility_raw._mapping["capacity"]
            
            event = facility_spec_parser(event)
            
            events.append(event)

    else:
        raise HTTPException(
            status_code=400, detail="only one param should be used")

    if subgroup is not None:
        subgroup_list = subgroup.split(",")
        subgroup_list.append("")
        result = [event for event in events
                  if event["subgroup"] in subgroup_list]

    else:
        result = events

    return result


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
            select(Facility.name, Facility.num, Facility.spec, Facility.capacity)
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
                         session: AsyncSession = Depends(get_session)):

    day: datetime = parser.parse(day)

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
