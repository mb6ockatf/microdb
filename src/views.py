from pprint import pprint as print
from datetime import datetime, timedelta
from aiohttp import web
from sqlalchemy import select, update, insert
from aiohttp_sqlalchemy import get_session
from models import Users, Payments


async def list_users_view_get(request):
    session = get_session(request)
    async with session.begin():
        result = await session.execute(select(Users))
        result = result.scalars()
    data = {}
    for instance in result:
        data[instance.user_id] = instance.subscription_until.isoformat()
    return web.json_response(data)


async def register(session, user_id: int):
    ref_string: str = str(hash(user_id))
    async with session.begin():
        result = await session.execute(
            insert(Users).values(
                user_id=user_id,
                subscription_until=datetime.now(),
                ref_string=ref_string),
            )


async def user_subscription_until_get(session, user_id: int) -> dict:
    async with session.begin():
        result = await session.execute(
                select(Users).where(Users.user_id == user_id)
                )
        result = result.scalars()
    return {"0": row.subscription_until for row in result}


async def subscribe(request) -> web.Response:
    user_id: int = int(request.rel_url.query["user_id"])
    subscription_delta_days: int = int(request.rel_url.query["days"])
    session = get_session(request)
    data: dict = await user_subscription_until_get(session, user_id)
    if len(data) == 0:
        result = await register(session, user_id)
        data = await user_subscription_until_get(session, user_id)
    previous_date = data["0"]
    delta = timedelta(days=subscription_delta_days)
    current_time = datetime.now()
    if previous_date >= current_time:
        previous_date += delta
    else:
        previous_date = current_time + delta
    async with session.begin():
        result = await session.execute(
            update(Users)
            .where(Users.user_id == user_id)
            .values(subscription_until=previous_date)
        )
        result = await session.execute(
            insert(Payments).values(user_id=user_id, datetime=current_time)
        )
    return web.json_response({"ok": "ok"})


async def subscription_check(request) -> web.Response:
    user_id: int = int(request.rel_url.query["user_id"])
    session = get_session(request)
    async with session.begin():
        result = await session.execute(
            select(Users).where(Users.user_id == user_id)
        )
        result = result.scalars()
    data = {"0": row.subscription_until for row in result}
    if len(data) == 0:
        return web.json_response({"result": False})
    if data["0"] >= datetime.now():
        return web.json_response({"result": True})
    return web.json_response({"result": False})

