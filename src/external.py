import httpx

from config import COOKIE, HOST, X_CSRF_TOKEN, X_REQUESTED_WITH


async def get_schedule(facility: str = None, 
                       group: str = None):
    
    client = httpx.AsyncClient()

    params = {
        "type": "agendaWeek",
        "groups[]": group,
        "facilityId": facility,
        "start": "2023-10-02T00:00:00",
        "end": "2023-10-07T00:00:00"
    }

    headers = {
        "Cookie": COOKIE,
        "X-CSRF-Token": X_CSRF_TOKEN,
        "X-Requested-With": X_REQUESTED_WITH 
    }

    req = await client.get(f"{HOST}/schedule/get", params=params, headers=headers)
    
    return req.json()