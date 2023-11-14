from database.database import get_session
from database.models import Group, Subgroup, User
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession
from src.api.auth import login_required

user_router = APIRouter(
    prefix="/user"
)


@user_router.post('/edit')
async def user_edit(group: str = None,
                    subgroup: str = None,
                    name: str = None,
                    color: str = None,
                    theme: str = None,
                    user=Depends(login_required),
                    session: AsyncSession = Depends(get_session)):  # email?

    edit_params = [group, subgroup, name, color, theme]
    edit_params_names = ["group", "subgroup", "name", "color", "theme"]

    user_update = {}

    if group != None:
        group_db = (await session.execute(
            select(Group).where(Group.name == group)
        )).first()

        if group_db == None:
            raise HTTPException(status_code=400, detail="group not found")

    if subgroup != None:

        if group == None:
            group = user.group

        subgroup_db = (await session.execute(
            select(Subgroup)
            .where(Subgroup.name == subgroup)
            .where(Subgroup.group == group)
        )).first()

        if subgroup_db == None:
            raise HTTPException(status_code=400, detail="subgroup not found")

    for i in range(len(edit_params)):
        if edit_params[i] != None:
            user_update[edit_params_names[i]] = edit_params[i]

    try:
        await session.execute(
            update(User).where(User.id == user.id).values(user_update)
        )
        await session.commit()
        return {"detail": "user edit success"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="server error")
