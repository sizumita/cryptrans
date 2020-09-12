from discord.ext import commands
import discord
from lib import CryptoModel, db, UserModel
from sqlalchemy.engine.url import URL


class Cryptrans(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or("ct."))
        self.loop.create_task(self.init_db())

    async def init_db(self):
        await db.set_bind(
            URL(
                drivername="postgresql",
                username="postgres",
                password="postgres",
                host="cryptrans_postgres",
                port="5430",
                database="cryptrans"
            )
        )
        await db.gino.create_all()

    async def on_ready(self):
        print('ready!')
        print(await UserModel().all())
        print(await UserModel().create(212513828641046529, 754191887203696732, 10))
        print(await UserModel().all())
        await db.pop_bind().close()
