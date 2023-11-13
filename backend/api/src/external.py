from typing import Union

import httpx
from dateutil import parser
from fastapi import HTTPException

from config import COOKIE, HOST, X_CSRF_TOKEN, X_REQUESTED_WITH


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


async def get_schedule(begin: str, end: str,
                       facility: str = None,
                       group: str = None,
                       teacher: str = None):

    client = httpx.AsyncClient()

    params = {
        "type": "agendaWeek",
        "groups[]": group,
        "facilityId": facility,
        "ppsId": teacher,
        "start": begin,
        "end": end
    }

    headers = {
        "Cookie": COOKIE,
        "X-CSRF-Token": X_CSRF_TOKEN,
        "X-Requested-With": X_REQUESTED_WITH
    }

    req = (await client.get(f"{HOST}/schedule/get", params=params, headers=headers)).json()

    if "events" in req:
        return {"events": await event_converter(req["events"]),
                "subgroups": len([x for x in req["subgroups"] if len(x) > 0])}

    else:
        return req