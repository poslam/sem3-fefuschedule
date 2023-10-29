import asyncio
from datetime import datetime, timedelta
from typing import Union

from dateutil import parser
from fastapi import Depends, HTTPException
from sqlalchemy import insert, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from database.models import Event, Facility, Group
from src.external import get_schedule


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

    while True:

        for group_raw in groups:

            group = group_raw._mapping

            temp = (await get_schedule(group=group["num"], begin=begin, end=end))

            await session.execute(
                update(Group).where(Group.num == group["num"]).values(
                    subgroups_count=temp["subgroups"])
            )
            await session.commit()

            for event in temp["events"]:

                event_db = await session.get(Event, event["event_id"])

                event_insert = {
                    "id": event["event_id"],
                    "name": event["event_name"],
                    "order": event["order"],
                    "begin": parser.parse(event["begin"]),
                    "end": parser.parse(event["end"]),
                    "facility": event["facility"],
                    "capacity": event["capacity"],
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

                facility = (await session.execute(
                    select(Facility).where(Facility.name == event["facility"])
                )).first()

                if facility is None:

                    max_num = max([x._mapping["num"] for x in (await session.execute(
                        select(Facility.num)
                    )).all()])

                    if event["spec"] == "Лекционные занятия":
                        spec = "lecture"
                    else:
                        spec = "lab_or_prac"

                    try:
                        await session.execute(
                            insert(Facility).values({"name": event["facility"],
                                                     "num": max_num + 1,
                                                     "spec": spec})
                        )
                        await session.commit()
                    except Exception as e:
                        await session.rollback()
                        print(e)

                    # отправка на почту?

                else:

                    if event["spec"] == "Лекционные занятия":
                        spec = "lecture"
                    else:
                        spec = "lab_or_prac"

                    try:
                        await session.execute(
                            update(Facility).where(Facility.name ==
                                                   event["facility"]).values(spec=spec)
                        )
                        await session.commit()
                    except Exception as e:
                        print(e)
                        await session.rollback()

                try:
                    await session.execute(stmt)
                    await session.commit()
                except Exception as e:
                    print(e)
                    await session.rollback()

            await asyncio.sleep(1)

        if end - datetime.utcnow() < timedelta(weeks=2):
            begin = begin + timedelta(7)
            end = end + timedelta(7)
        else:
            await asyncio.sleep(2 * 24 * 60 * 60)  # sleep for 2 days


def facility_spec_parser(dict: dict):

    try:
        spec = dict["spec"]
    except BaseException:
        raise HTTPException(status_code=500, detail="incorrect spec")

    if spec == "lab_or_prac":
        spec_new = "Обычная аудитория"

    elif spec == "lecture":
        spec_new = "Лекционная аудитория"

    dict["spec"] = spec_new

    return dict


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
#     },
