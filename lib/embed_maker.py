from discord import Embed
from discord.ext import commands


class EmbedMaker:
    def __init__(self, ctx: commands.Context):
        self.ctx = ctx
        self.embed = None

    def set_author(self):
        if self.embed is not None:
            self.embed.set_author(
                name=self.ctx.author.display_name,
                icon_url=self.ctx.author.avatar_url_as(format="png")
            )
        return self

    def success(self, embed: Embed):
        embed.colour = 0x2196F3
        self.embed = embed
        return self

    def error(self, embed: Embed):
        embed.colour = 0xF44336
        self.embed = embed
        return self

    def default(self, embed: Embed):
        embed.colour = 0x00C853
        self.embed = embed
        return self

    def by_error_text(self, text: str):
        self.error(
            embed=Embed(
                description="\U0000274c " + text
            )
        )
        return self

    def by_success_text(self, text: str):
        self.success(
            embed=Embed(
                description="\U00002611 " + text
            )
        )
        return self

    async def send(self):
        if self.embed is None:
            return

        self.set_author()
        await self.ctx.send(embed=self.embed)
