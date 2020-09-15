from discord.ext import commands
from os import environ
from lib import db
from models import CryptoModel, Crypto
from sqlalchemy.engine.url import URL
import asyncio
from lib import EmbedMaker


wiki_commands = {
    "info": "https://github.com/sizumita/virtualCrypto/wiki/Commands#vcinfo-通貨名",
    "pay": "https://github.com/sizumita/virtualCrypto/wiki/Commands#vcpaytipsend-メンション-通貨の単位-数量",
    "create": "https://github.com/sizumita/virtualCrypto/wiki/Commands#vccreate-通貨名-通貨の単位-10分に増える通貨の量",
    "give": "https://github.com/sizumita/virtualCrypto/wiki/Commands#vcgive-メンション-数量",
}


class VirtualCrypto(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or("vc."), help_command=None)
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
                *[crypto.update(hold=Crypto.hold + crypto.per_amount).apply() for crypto in await CryptoModel().all()
                  if crypto.distribution],
                loop=self.loop
            )

    async def on_command_error(self, context: commands.Context, exception):
        if isinstance(exception, commands.BadArgument) or isinstance(exception, commands.MissingRequiredArgument):
            if context.command.name in wiki_commands.keys():
                await EmbedMaker(context).by_error_text("コマンドの引数が間違っています。こちらからご確認ください: " + wiki_commands[context.command.name]).send()
                return
        if isinstance(exception, commands.CommandNotFound):
            return

        await super(VirtualCrypto, self).on_command_error(context, exception)
