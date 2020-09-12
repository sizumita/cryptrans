from discord.ext import commands


class Cryptrans(commands.Bot):
    def __init__(self) -> None:
        super().__init__(command_prefix=commands.when_mentioned_or("ct."))
