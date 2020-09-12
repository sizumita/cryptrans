from discord.ext import commands
from os import environ
from lib import db
from models import CryptoModel, Crypto
from sqlalchemy.engine.url import URL
import asyncio


class Cryptrans(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or("vc."))
        self.loop.create_task(self.init_db())
        self.loop.create_task(self.give_hold_batch())

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

    async def give_hold_batch(self):
        await self.wait_until_ready()
        while not self.is_closed():
            await asyncio.sleep(60 * 10)

            await asyncio.gather(
                *[crypto.update(hold=Crypto.hold + crypto.per_amount).apply() for crypto in await CryptoModel().all()],
                loop=self.loop
            )
