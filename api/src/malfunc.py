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


import asyncio
from typing import Union

from dateutil import parser
from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session


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

        except:
            raise HTTPException(status_code=400, detail="incorrect event format")
        
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

            except:
                raise HTTPException(status_code=400, detail="incorrect event format")
            
        return result
        
    else:
        raise HTTPException(status_code=400, detail="incorrect event format")\
        

async def event_updater(session: AsyncSession = Depends(get_session)):
    
    while True:
        pass

        await asyncio.sleep(10)