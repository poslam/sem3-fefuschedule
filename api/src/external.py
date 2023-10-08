import httpx
from src.malfunc import event_converter

from config import COOKIE, HOST, X_CSRF_TOKEN, X_REQUESTED_WITH


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
    
        return await event_converter(req["events"])
    
    else:
        
        return req