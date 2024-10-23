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


async def subscribe(request):
    user_id: int = int(request.rel_url.query["user_id"])
    subscription_delta_days: int = int(request.rel_url.query["days"])
    session = get_session(request)
    async with session.begin():
        result = await session.execute(
            select(Users).where(Users.user_id == user_id)
        )
        result = result.scalars()
    data = {"0": row.subscription_until for row in result}
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
