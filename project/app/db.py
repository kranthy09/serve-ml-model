"""
database connection for App.
"""

import os
import logging


from fastapi import FastAPI
from tortoise import Tortoise, run_async
from tortoise.contrib.fastapi import RegisterTortoise


log = logging.getLogger("uvicorn")

TORTOISE_ORM = {
    "connections": {"default": os.environ.get("DATABASE_URL")},
    "apps": {
        "models": {
            "models": ["app.models.tortoise", "aerich.models"],
            "default_connection": "default",
        },
    },
}


# def init_db(app: FastAPI) -> None:
#     """Database initializer for application models."""

#     RegisterTortoise(
#         app,
#         db_url=os.environ.get("DATABASE_URL"),
#         modules={"models": ["app.models.tortoise"]},
#         generate_schemas=False,
#         add_exception_handlers=True,
#     )


# class tortoise.contrib.fastapi.RegisterTortoise(app, config=None, config_file=None, db_url=None, modules=None, generate_schemas=False, add_exception_handlers=False, use_tz=False, timezone='UTC', _create_db=False)[source]
async def generate_schemas() -> None:
    """Apply schema to the database in app's final state."""

    log.info("Initializing Tortoise...")

    await Tortoise.init(
        db_url=os.environ.get("DATABASE_URL"),
        modules={"models": ["models.tortoise"]},
    )
    log.info("Generating database schema via Tortoise...")
    await Tortoise.generate_schemas()
    await Tortoise.close_connections()


if __name__ == "__main__":
    log.info("Running database schema generation...")
    run_async(generate_schemas())
