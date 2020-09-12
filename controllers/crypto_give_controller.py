from discord.ext import commands
import discord
from models import UserModel, CryptoModel, Crypto


class CryptoGiveController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def give(self, ctx: commands.Context, member: discord.Member, amount: int):
        """
        通貨を配布します。これは未配布の通貨から支払われます。
        """
        crypto = await CryptoModel().get(ctx.guild.id)
        if crypto is None:
            await ctx.send("このサーバーでは通貨は発行されていません。")
            return

        if amount > crypto.hold:
            await ctx.send(f"未配布の通貨が足りません。({amount}{crypto.unit} > {crypto.hold}{crypto.unit})")
            return
        if await UserModel().add_amount(member.id, ctx.guild.id, amount):
            await crypto.update(hold=Crypto.hold - amount).apply()
            await ctx.send(f"{ctx.author.mention}さんにより{member.mention}さんに{amount}{crypto.unit}付与しました。"
                           f"\n`vc.me`コマンドから確認してください。")
            return

        await ctx.send("処理に失敗しました。再度実行してください。")


def setup(bot):
    return bot.add_cog(CryptoGiveController(bot))
