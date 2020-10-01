from discord.ext import commands
from os import environ
from lib import db
from models import CryptoModel, Crypto, UserModel
from sqlalchemy.engine.url import URL
import asyncio
from lib import EmbedMaker
import discord
import traceback


wiki_commands = {
    "info": "https://github.com/virtualCrypto-discord/virtualCrypto/wiki/Commands#vcinfo-通貨名",
    "pay": "https://github.com/virtualCrypto-discord/virtualCrypto/wiki/Commands#vcpaytipsend-メンション-通貨の単位-数量",
    "create": "https://github.com/virtualCrypto-discord/virtualCrypto/wiki/Commands#vccreate-通貨名-通貨の単位-10分に増える通貨の量",
    "give": "https://github.com/virtualCrypto-discord/virtualCrypto/wiki/Commands#vcgive-メンション-数量",
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
            crypts = await CryptoModel().all()
            try:
                for crypto in crypts:
                    if not crypto.distribution:
                        continue
                    all_amount = sum([i.amount for i in await UserModel().get_crypto_all(crypto.id)])
                    online_count = len(
                        [member for member in (self.get_guild(crypto.id).members if self.get_guild(crypto.id) is not None else 0) if
                         member.status is not discord.Status.offline
                         and member.status is not discord.Status.idle
                         and not member.bot]
                    )
                    if all_amount + (online_count * 10) > crypto.max_amount:
                        self.loop.create_task(
                            crypto.update(
                                hold=Crypto.hold + (crypto.max_amount - (online_count * 10)),
                                distribution=False).apply()
                        )
                        continue

                    self.loop.create_task(
                        crypto.update(hold=Crypto.hold + (online_count * 10)).apply()
                    )
            except Exception as e:
                await self.mention_error(e)
            await asyncio.sleep(60 * 60)  # 60 minutes

    async def on_command_error(self, context: commands.Context, exception):
        if isinstance(exception, commands.BadArgument) or isinstance(exception, commands.MissingRequiredArgument):
            if context.command.name in wiki_commands.keys():
                await EmbedMaker(context).by_error_text("コマンドの引数が間違っています。こちらからご確認ください: " + wiki_commands[context.command.name]).send()
                return
        if isinstance(exception, commands.CommandNotFound):
            return

        await self.mention_error(exception)

    async def mention_error(self, exception: Exception):
        embed = discord.Embed(
            title=str(exception),
            description="\n".join(traceback.format_exception(type(exception), exception, exception.__traceback__))[:1500]
        )
        await self.get_channel(757236120475009108).send("<@212513828641046529>", embed=embed)
