import asyncio
from datetime import datetime, timedelta
from typing import Union
from uuid import uuid4

from database.database import get_session
from database.models import (Event, Facility, Group, SpecialEvent, Subgroup,
                             Teacher)
from dateutil import parser
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.external import get_schedule


def time():
    return datetime.utcnow()+timedelta(hours=10)


async def event_converter(obj: Union[dict, list]):

    if isinstance(obj, dict):

        try:

            event = {
                "event_id": obj["id"],
                "event_name": obj["title"],
                "order": obj["order"],
                "begin": parser.parse(obj["start"]).strftime("%Y-%m-%dT%H:%M:%S"),
                "end": parser.parse(obj["end"]).strftime("%Y-%m-%dT%H:%M:%S"),
                "facility": obj["classroom"],
                "spec": obj["pps_load"],
                "capacity": obj["students_number"],
                "teacher": obj["teacher"],
                "group": obj["group"],
                "subgroup": obj["subgroup"]
            }

            return event

        except BaseException:
            raise HTTPException(
                status_code=400, detail="incorrect event format")

    elif isinstance(obj, list):
        result = []

        for event_raw in obj:

            try:

                event = {
                    "event_id": event_raw["id"],
                    "event_name": event_raw["title"],
                    "order": event_raw["order"],
                    "begin": parser.parse(event_raw["start"]).strftime("%Y-%m-%dT%H:%M:%S"),
                    "end": parser.parse(event_raw["end"]).strftime("%Y-%m-%dT%H:%M:%S"),
                    "facility": event_raw["classroom"],
                    "spec": event_raw["pps_load"],
                    "capacity": event_raw["students_number"],
                    "teacher": event_raw["teacher"],
                    "group": event_raw["group"],
                    "subgroup": event_raw["subgroup"]
                }

                result.append(event)

            except BaseException:
                raise HTTPException(
                    status_code=400, detail="incorrect event format")

        return result

    else:
        raise HTTPException(status_code=400, detail="incorrect event format")


async def event_updater(session: AsyncSession = Depends(get_session)):

    groups = (await session.execute(
        select(Group.name, Group.num)
    )).all()

    while True:

        day = datetime.utcnow()

        day_num = day.weekday()

        end = day

        while (day_num < 6):
            day_num += 1
            end = end + timedelta(days=1)

        begin = end - timedelta(days=6)

        time_periods = []

        for i in range(0, 5):
            time_periods.append(
                [begin+timedelta(weeks=i), end+timedelta(weeks=i)])

        for period in time_periods:

            for group_raw in groups:

                try:

                    group = group_raw._mapping

                    temp = (await get_schedule(group=group["num"], begin=period[0], end=period[1]))

                    for event in temp["events"]:

                        facility = (await session.execute(
                            select(Facility).where(
                                Facility.name == event["facility"])
                        )).first()

                        if facility != None:
                            capacity = max(
                                facility[0].capacity, event["capacity"])
                        else:
                            capacity = event["capacity"]
                            
                        if event["spec"] in ["Лабораторные работы", "Практические занятия"]:
                            spec = "lab_or_prac"

                        elif event["spec"] == "Лекционные занятия":
                            spec = "lecture"

                        else:
                            spec = "unknown"

                        event_db = await session.get(Event, event["event_id"])

                        event_insert = {
                            "id": event["event_id"],
                            "name": event["event_name"],
                            "order": event["order"],
                            "begin": parser.parse(event["begin"]),
                            "end": parser.parse(event["end"]),
                            "facility": event["facility"],
                            "spec": spec,
                            "capacity": capacity,
                            "teacher": event["teacher"],
                            "group": event["group"],
                            "subgroup": event["subgroup"]
                        }

                        if event_db is not None:
                            if event_db.changed:
                                continue
                            else:
                                stmt = (update(Event)
                                        .where(Event.id == event["event_id"])
                                        .values(event_insert)
                                        )
                        else:
                            stmt = insert(Event).values(event_insert)

                        teacher = (await session.execute(
                            select(Teacher).where(
                                Teacher.name == event["teacher"])
                        )).first()

                        if teacher is None:
                            try:
                                await session.execute(
                                    insert(Teacher).values({"id": str(uuid4()),
                                                            "name": event["teacher"]})
                                )
                                await session.commit()
                            except Exception as e:
                                print(e)
                                await session.rollback()

                        if facility is None:

                            max_num = max([x._mapping["num"] for x in (await session.execute(
                                select(Facility.num)
                            )).all()])

                            if event["capacity"] >= 50:
                                spec = "lecture"
                            else:
                                spec = "lab_or_prac"

                            try:
                                await session.execute(
                                    insert(Facility).values({"name": event["facility"],
                                                            "num": max_num + 1,
                                                             "spec": spec,
                                                             "capacity": event["capacity"]})
                                )
                                await session.commit()
                                await session.commit()
                            except Exception as e:
                                print(e)
                                await session.rollback()
                                raise HTTPException(
                                    status_code=500, detail="server error")

                        else:

                            if facility[0].spec != 'lecture':

                                if capacity >= 50:
                                    spec = "lecture"
                                else:
                                    spec = "lab_or_prac"

                            try:
                                await session.execute(
                                    update(Facility).where(Facility.name ==
                                                           event["facility"])
                                    .values({"spec": spec,
                                            "capacity": capacity})
                                )
                                await session.execute(stmt)
                                await session.commit()
                            except Exception as e:
                                print(e)
                                await session.rollback()
                                raise HTTPException(
                                    status_code=500, detail="server error")

                    for subgroup_name in temp["subgroups"]:

                        subgroup = (await session.execute(
                            select(Subgroup)
                            .where(Subgroup.name == subgroup_name)
                            .where(Subgroup.group == group["name"])
                        )).first()

                        subgroup_insert = {
                            "name": subgroup_name,
                            "group": group["name"]
                        }

                        if subgroup == None:
                            try:
                                await session.execute(
                                    insert(Subgroup).values(subgroup_insert)
                                )
                                await session.commit()
                            except Exception as e:
                                print(e)
                                await session.rollback()
                                raise HTTPException(
                                    status_code=500, detail="server error")

                except Exception as e:
                    print(e)

                await asyncio.sleep(0.5)


def event_spec_parser(obj: dict):

    try:
        spec = obj["spec"].name
    except Exception as e:
        spec = 'unknown'

    if spec == "lab_or_prac":
        spec_new = "Практическое или лабораторное занятие"

    elif spec == "lecture":
        spec_new = "Лекционное занятие"

    else:
        spec_new = "Неизвестно"

    obj = dict(obj)
    obj["spec"] = spec_new

    return obj


def facility_spec_parser(obj: dict):

    try:
        spec = obj["spec"].name
    except BaseException:
        spec = 'unknown'

    if spec == "lab_or_prac":
        spec_new = "Обычная аудитория"

    elif spec == "lecture":
        spec_new = "Лекционная аудитория"

    else:
        spec_new = "Обычная аудитория"

    obj = dict(obj)
    obj["spec"] = spec_new

    return obj


async def special_event_checker(obj: dict,
                                session: AsyncSession = Depends(get_session)):

    special_event_rule = (await session.execute(
        select(SpecialEvent)
        .where(SpecialEvent.group == obj["group"])
        .where(SpecialEvent.name == obj["event_name"])
    )).first()

    if special_event_rule != None:
        obj["subgroup"] = ""

    return obj


async def event_filter(event: dict,
                       session: AsyncSession = Depends(get_session)):

    event = event_spec_parser(event)
    event = await special_event_checker(event, session)

    return event


# {
#         "id": 10782062,
#         "guid": "96fbe9b4-d9fc-4636-a89b-434a7d877f3d",
#         "team_guid": "c2eb99e2-8e8c-4bcb-b5a5-5f16e9a03657",
#         "title": "Базы данных",
#         "start": "2023-10-24T10:10:00+10:00",
#         "end": "2023-10-24T11:40:00+10:00",
#         "academicGroupId": 5549,
#         "academicGroupGuid": "d2599693-5d99-11ec-a216-00155d20357c",
#         "classroom": "D546",
#         "control_type": "",
#         "disciplineId": 5856,
#         "distanceEducationDescription": "",
#         "distanceEducationURL": null,
#         "group": "Б9122-01.03.02сп",
#         "group_id": 5549,
#         "order": 2,
#         "pps_load": "Лабораторные работы",
#         "specialization": "Системное программирование",
#         "specialization_id": 46,
#         "students_number": 18,
#         "subgroup": "1",
#         "subgroup_id": 49,
#         "teacher": "Месенев Павел Ростиславович",
#         "teacher_degree": "",
#         "userId": 21465
# }
