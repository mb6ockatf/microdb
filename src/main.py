#!/usr/bin/env python3
from aiohttp import web
from sqlalchemy import MetaData, orm
from aiohttp_sqlalchemy import setup, bind, init_db, get_session
from settings import config
from views import list_users_view_get, subscribe, subscription_check


async def main():
    return ""


async def app_factory():
    application = web.Application()
    application["config"] = config
    metadata = MetaData()
    Base = orm.declarative_base(metadata=metadata)
    application.router.add_view("/api_v1/list_users", list_users_view_get)
    setup(
        application,
        [
            bind(application["config"]["postgres"]["database_url"]),
        ],
    )
    await init_db(application, metadata)
    application.add_routes(
        [
            web.get("/", main),
            web.get("/api_v1/subscribe", subscribe),
            web.get("/api_v1/subscription_check", subscription_check),
        ]
    )
    return application


if __name__ == "__main__":
    web.run_app(app_factory(), port=config["common"]["port"])
