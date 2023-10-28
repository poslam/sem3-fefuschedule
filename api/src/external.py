import httpx
from config import COOKIE, HOST, X_CSRF_TOKEN, X_REQUESTED_WITH
from src.malfunc import event_converter


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