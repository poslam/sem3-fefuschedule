from database.database import get_session
from database.models import Event, Facility, Group, Subgroup, Teacher
from dateutil import parser
from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy import insert, select, update
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
                   Event.spec,
                   Event.capacity,
                   Event.teacher,
                   Event.group,
                   Event.subgroup)
            .where(Event.begin >= begin)
            .where(Event.end <= end)
            .where(Event.active == True)
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
    try:
        data = await request.json()

        event_name = data["event_name"]
        order = data["order"]
        begin = parser.parse(data["begin"])
        end = parser.parse(data["end"])
        facility_name = data["facility"]
        spec = data["spec"]
        teacher_name = data["teacher"]
        group_name = data["group"]
        subgroup_name = data["subgroup"]

    except:
        raise HTTPException(status_code=400, detail="incorrect request")

    if order > 8:
        raise HTTPException(status_code=400,
                            detail="incorrect paramteter(s): order. order must be <= 8")

    if begin.date() != end.date():
        raise HTTPException(status_code=400,
                            detail="incorrect parameter(s): begin, end. begin and end should be at one day")

    facility = (await session.execute(
        select(Facility).where(Facility.name == facility_name)
    )).first()

    if facility == None:
        raise HTTPException(status_code=400, detail="facility not found")

    teacher = (await session.execute(
        select(Teacher).where(Teacher.name == teacher_name)
    )).first()

    if teacher == None:
        raise HTTPException(status_code=400, detail="teacher not found")

    group = (await session.execute(
        select(Group).where(Group.name == group_name)
    )).first()

    if group == None:
        raise HTTPException(status_code=400, detail="group not found")

    if subgroup_name != "":

        subgroup = (await session.execute(
            select(Subgroup)
            .where(Subgroup.name == subgroup_name)
            .where(Subgroup.group == group_name)
        )).first()

        if subgroup == None:
            raise HTTPException(status_code=400, detail="subgroup not found")
        
    else:
        subgroup = ""

    if spec not in ["lab_or_prac", "lecture"]:
        raise HTTPException(status_code=400,
                            detail="incorrect parameter(s): spec. must be 'lab_or_prac' or 'lecture")

    event_insert = {
        "name": event_name,
        "order": order,
        "begin": begin,
        "end": end,
        "facility": facility_name,
        "spec": spec,
        "teacher": teacher_name,
        "group": group_name,
        "subgroup": subgroup_name
    }

    try:
        await session.execute(
            insert(Event).values(event_insert)
        )
        await session.commit()
        return {"detail": "event add success"}
    except Exception as e:
        print(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="server error")


@event_router.post('/edit')
async def event_edit(event_id: int,
                     request: Request,
                     user=Depends(elder_required),
                     session: AsyncSession = Depends(get_session)):

    try:
        data = await request.json()

        event_name = data["event_name"]
        order = data["order"]
        begin = parser.parse(data["begin"])
        end = parser.parse(data["end"])
        facility_name = data["facility"]
        spec = data["spec"]
        teacher_name = data["teacher"]
        group_name = data["group"]
        subgroup_name = data["subgroup"]

    except:
        raise HTTPException(status_code=400, detail="incorrect request")

    event = await session.get(Event, event_id)

    if event == None:
        raise HTTPException(status_code=400, detail="event not found")

    if order > 8:
        raise HTTPException(status_code=400,
                            detail="incorrect paramteter(s): order. order must be <= 8")

    if begin.date() != end.date():
        raise HTTPException(status_code=400,
                            detail="incorrect parameter(s): begin, end. begin and end should be at one day")

    facility = (await session.execute(
        select(Facility).where(Facility.name == facility_name)
    )).first()

    if facility == None:
        raise HTTPException(status_code=400, detail="facility not found")

    teacher = (await session.execute(
        select(Teacher).where(Teacher.name == teacher_name)
    )).first()

    if teacher == None:
        raise HTTPException(status_code=400, detail="teacher not found")

    group = (await session.execute(
        select(Group).where(Group.name == group_name)
    )).first()

    if group == None:
        raise HTTPException(status_code=400, detail="group not found")

    if subgroup_name != "":

        subgroup = (await session.execute(
            select(Subgroup)
            .where(Subgroup.name == subgroup_name)
            .where(Subgroup.group == group_name)
        )).first()

        if subgroup == None:
            raise HTTPException(status_code=400, detail="subgroup not found")
        
    else:
        subgroup = ""

    if spec not in ["lab_or_prac", "lecture"]:
        raise HTTPException(status_code=400,
                            detail="incorrect parameter(s): spec. must be 'lab_or_prac' or 'lecture")

    event_insert = {
        "name": event_name,
        "order": order,
        "begin": begin,
        "end": end,
        "facility": facility_name,
        "spec": spec,
        "teacher": teacher_name,
        "group": group_name,
        "subgroup": subgroup_name,
        "changed": True
    }

    try:
        await session.execute(
            update(Event)
            .where(Event.id == event_id)
            .values(event_insert)
        )
        await session.commit()
        return {"detail": "event edit success"}
    except Exception as e:
        print(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="server error")


@event_router.post('/delete')
async def event_delete(event_id: int,
                       user=Depends(elder_required),
                       session: AsyncSession = Depends(get_session)):

    event = await session.get(Event, event_id)

    if event == None:
        raise HTTPException(status_code=400, detail="event not found")

    try:
        await session.execute(
            update(Event)
            .where(Event.id == event_id)
            .values({"changed": True,
                     "active": False})
        )
        await session.commit()
        return {"detail": "event delete success"}
    except Exception as e:
        print(e)
        await session.rollback()
        raise HTTPException(status_code=500, detail="server error")
