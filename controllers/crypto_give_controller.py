from discord.ext import commands
import discord
from models import UserModel, CryptoModel, Crypto


class CryptoGiveController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.user_model = UserModel()
        self.crypto_model = CryptoModel()

    @commands.command()
    @commands.guild_only()
    @commands.has_guild_permissions(administrator=True)
    async def give(self, ctx: commands.Context, member: discord.Member, amount: int):
        """
        通貨を配布します。これは未配布の通貨から支払われます。
        """
        if member.bot:
            await ctx.send("Botを指定することはできません。")
            return

        crypto = await self.crypto_model.get(ctx.guild.id)
        if crypto is None:
            await ctx.send("このサーバーでは通貨は発行されていません。")
            return

        if amount > crypto.hold:
            await ctx.send(f"未配布の通貨が足りません。({amount}{crypto.unit} > {crypto.hold}{crypto.unit})")
            return
        if await self.user_model.add_amount(member.id, ctx.guild.id, amount):
            await crypto.update(hold=Crypto.hold - amount).apply()
            await ctx.send(f"{ctx.author.mention}さんにより{member.mention}さんに{amount}{crypto.unit}付与しました。"
                           f"\n`vc.me`コマンドから確認してください。")
            return

        await ctx.send("処理に失敗しました。再度実行してください。")

    @commands.command(aliases=["pay"])
    async def tip(self, ctx: commands.Context, member: discord.Member, unit: str, amount: int):
        """
        unitで指定した通貨を渡します。
        """
        if member.bot:
            await ctx.send("Botを指定することはできません。")
            return

        crypto = await self.crypto_model.get_by_unit(unit)
        if crypto is None:
            await ctx.send("その単位の通貨は存在しません。")
            return

        user = await self.user_model.get_one(ctx.author.id, crypto.id)

        if user is None:
            await ctx.send("あなたはその通貨を所持していません。")
            return

        if amount > user.amount:
            await ctx.send(f"所持数が足りません。({amount}{crypto.unit} > {user.amount}{crypto.unit})")
            return

        await self.user_model.add_amount(ctx.author.id, crypto.id, -amount)
        await self.user_model.add_amount(member.id, crypto.id, amount)

        await ctx.send(f"{ctx.author.mention}さんから{member.mention}さんへ{amount}{crypto.unit}送られました。\n"
                       f"`vc.me`コマンドから確認してください。")


def setup(bot):
    return bot.add_cog(CryptoGiveController(bot))
