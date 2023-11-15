from database.database import get_session
from database.models import Event, Facility, Group, Teacher
from dateutil import parser
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.auth import elder_required, shared
from src.utils import event_filter

event_router = APIRouter(
    prefix="/event"
)


@event_router.get("/view")
async def schedule(begin: str, end: str,
                   facility_name: str = None,
                   group_name: str = None,
                   teacher_name: str = None,
                   subgroup: str = None,  # 3 or 3,4,5
                   user=Depends(shared),
                   session: AsyncSession = Depends(get_session)):

    begin = parser.parse(begin)
    end = parser.parse(end)

    stmt = (select(Event.id.label("event_id"),
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
            .where(Facility.name == Event.facility)
            .where(Event.begin >= begin)
            .where(Event.end <= end)
            .order_by(Event.begin))

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

        events_raw = (await session.execute(stmt.where(Event.facility == facility))).all()

        events = []

        for event_raw in events_raw:

            event = dict(event_raw._mapping)

            event["capacity"] = facility_raw._mapping["capacity"]

            event = await event_filter(event, session)

            events.append(event)

    elif group_name is not None and all(x is None for x in [teacher_name, facility_name]):

        group_raw = (await session.execute(
            select(Group.name).where(Group.name == group_name)
        )).first()

        if group_raw is None:
            raise HTTPException(status_code=400, detail="group not found")

        group = group_raw._mapping["name"]

        events_raw = (await session.execute(stmt.where(Event.group == group))).all()

        events = []

        for event_raw in events_raw:

            event = dict(event_raw._mapping)

            facility_raw = (await session.execute(
                select(Facility.capacity).where(
                    Facility.name == event["facility"])
            )).first()

            if facility_raw != None:
                event["capacity"] = facility_raw._mapping["capacity"]

            event = await event_filter(event, session)

            events.append(event)

    elif teacher_name is not None and all(x is None for x in [group_name, facility_name]):

        teacher_raw = (await session.execute(
            select(Teacher.name).filter(
                Teacher.name.ilike('%' + teacher_name + '%'))
        )).first()

        if teacher_raw is None:
            raise HTTPException(status_code=400, detail="teacher not found")

        teacher = teacher_raw._mapping["name"]

        events_raw = (await session.execute(stmt.where(Event.teacher == teacher))).all()

        events = []

        for event_raw in events_raw:

            event = dict(event_raw._mapping)

            facility_raw = (await session.execute(
                select(Facility.capacity).where(
                    Facility.name == event["facility"])
            )).first()

            if facility_raw != None:
                event["capacity"] = facility_raw._mapping["capacity"]

            event = await event_filter(event, session)

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


@event_router.post('/add')
async def event_add(request: Request,
                    user=Depends(elder_required),
                    session: AsyncSession = Depends(get_session)):
    pass


@event_router.post('/edit')
async def event_edit(user=Depends(elder_required)):
    pass


@event_router.post('/delete')
async def event_delete(user=Depends(elder_required)):
    pass
