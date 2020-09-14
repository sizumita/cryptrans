from discord.ext import commands
from models import UserModel, CryptoModel, Crypto
from lib import EmbedMaker
import discord


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
            await EmbedMaker(ctx).by_error_text("Botを指定することはできません。").send()
            return

        if amount <= 0:
            await EmbedMaker(ctx).by_error_text("0以下の数を指定することはできません。").send()
            return

        crypto = await self.crypto_model.get(ctx.guild.id)
        if crypto is None:
            await EmbedMaker(ctx).by_error_text("このサーバーでは通貨は発行されていません。").send()
            return

        if amount > crypto.hold:
            await EmbedMaker(ctx).by_error_text(
                f"未配布の通貨が足りません。({amount}{crypto.unit} > {crypto.hold}{crypto.unit})").send()
            return
        if await self.user_model.add_amount(member.id, ctx.guild.id, amount):
            await crypto.update(hold=Crypto.hold - amount).apply()
            await EmbedMaker(ctx).by_success_text(
                f"{ctx.author.mention}さんにより{member.mention}さんに{amount}{crypto.unit}付与しました。"
                f"\n`vc.me`コマンドから確認してください。").send()
            return

        await EmbedMaker(ctx).by_error_text("処理に失敗しました。再度実行してください。").send()

    @commands.command(aliases=["pay", "send"])
    async def tip(self, ctx: commands.Context, member: discord.Member, unit: str, amount: int):
        """
        unitで指定した通貨を渡します。
        """
        if member.bot:
            await EmbedMaker(ctx).by_error_text("Botを指定することはできません。").send()
            return

        if member.id == ctx.author.id:
            await EmbedMaker(ctx).by_error_text("自分自身を指定することはできません。").send()
            return

        if amount <= 0:
            await EmbedMaker(ctx).by_error_text("0以下の数を指定することはできません。").send()
            return

        crypto = await self.crypto_model.get_by_unit(unit)
        if crypto is None:
            await EmbedMaker(ctx).by_error_text("その単位の通貨は存在しません。").send()
            return

        user = await self.user_model.get_one(ctx.author.id, crypto.id)

        if user is None:
            await EmbedMaker(ctx).by_error_text("あなたはその通貨を所持していません。").send()
            return

        if amount > user.amount:
            await EmbedMaker(ctx).by_error_text(
                f"所持数が足りません。({amount}{crypto.unit} > {user.amount}{crypto.unit})").send()
            return

        await self.user_model.add_amount(ctx.author.id, crypto.id, -amount)
        await self.user_model.add_amount(member.id, crypto.id, amount)

        await EmbedMaker(ctx).by_success_text(
            f"{ctx.author.mention}さんから{member.mention}さんへ{amount}{crypto.unit}送られました。\n"
            f"`vc.me`コマンドから確認してください。").send()


def setup(bot):
    return bot.add_cog(CryptoGiveController(bot))
