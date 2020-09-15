from discord.ext import commands
from models import CryptoModel, UserModel
import discord
from lib import EmbedMaker


class CryptoInfoController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def info(self, ctx: commands.Context, unit=None):
        if unit is None:
            crypto = await CryptoModel().get(ctx.guild.id)

            if crypto is None:
                await EmbedMaker(ctx).by_error_text("このサーバーでは通貨は作成されていません。").send()
                return

        else:
            crypto = await CryptoModel().get_by_unit(unit)

            if crypto is None:
                await EmbedMaker(ctx).by_error_text("その単位の通貨は作成されていません。").send()
                return

        all_users = await UserModel().get_crypto_all(crypto.id)
        guild = self.bot.get_guild(crypto.id)
        total_amount = sum(user.amount for user in all_users)

        embed = discord.Embed(
            title=f"{crypto.name} の情報"
        )
        embed.add_field(
            name="単位",
            value=f"`{crypto.unit}`",
            inline=False
        )
        embed.add_field(
            name="総量(まだ配布されていない枚数もカウントされています)",
            value=f"{total_amount + crypto.hold}{crypto.unit}",
            inline=False
        )
        embed.add_field(
            name="配布総量",
            value=f"{total_amount}{crypto.unit}",
            inline=False
        )
        embed.add_field(
            name="配布されていない量",
            value=f"{crypto.hold}{crypto.unit}",
            inline=False
        )
        embed.add_field(
            name="10分ごとの増加量",
            value=f"{crypto.per_amount}{crypto.unit}",
            inline=False
        )
        embed.add_field(
            name="配布元サーバー",
            value=f"{guild.name if guild is not None else '情報の取得に失敗しました。'}",
            inline=False
        )
        await ctx.send(embed=embed)


def setup(bot):
    return bot.add_cog(CryptoInfoController(bot))
