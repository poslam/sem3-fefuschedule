from fastapi import FastAPI

from src.api.api import api_router


app = FastAPI()

app.include_router(api_router)


# @app.on_event("startup")
# async def startup_event(back: BackgroundTasks,
#                         session: AsyncSession = Depends(get_session)):
#     back.add_task(event_updater, session)
