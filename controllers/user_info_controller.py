from discord.ext import commands
from models import UserModel, CryptoModel
import discord


class UserInfoController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_model = UserModel()
        self.crypto_model = CryptoModel()

    @commands.command()
    async def me(self, ctx: commands.Context):
        users = await self.user_model.get(ctx.author.id)
        if not users:
            await ctx.send("あなたは一つも通貨を持っていません。")
            return

        text = ""
        for user in users:
            crypto = await self.crypto_model.get(user.guild_id)
            text += f"`{crypto.name}` - **{user.amount}{crypto.unit}**\n"

        embed = discord.Embed(
            title="所持通貨一覧",
            description=text,
        )
        await ctx.send(embed=embed)


def setup(bot):
    return bot.add_cog(UserInfoController(bot))
