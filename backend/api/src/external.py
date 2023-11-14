from fastapi import HTTPException
import httpx
from src.utils import event_converter
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

    req = (await client.get(f"{HOST}/schedule/get", params=params, headers=headers,
                            timeout=600)).json()

    if "events" in req:
        return {"events": await event_converter(req["events"]),
                "subgroups": [x for x in req["subgroups"] if len(x) > 0]}

    else:
        return req


async def get_user_info(ya_token: str):
    
    client = httpx.AsyncClient()
    
    headers = {
        "Authorization": f"OAuth {ya_token}"
    }
    
    req = (await client.get("https://login.yandex.ru/info", headers=headers))
    
    if req.status_code == 200:
        return req
    
    else:
        raise HTTPException(status_code=400, detail="incorrect ya_token")