from discord.ext import commands
from os import environ
from lib import db
from sqlalchemy.engine.url import URL


class Cryptrans(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or("vc."))
        self.loop.create_task(self.init_db())

    async def init_db(self):
        await db.set_bind(
            URL(
                drivername="postgresql",
                username=environ.get("POSTGRES_USER"),
                password=environ.get("POSTGRES_PASSWORD"),
                host="virtualcrypto_postgres",
                port="5430",
                database=environ.get("POSTGRES_DB")
            )
        )
        await db.gino.create_all()
