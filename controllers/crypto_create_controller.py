from models import CryptoModel
from discord.ext import commands
from lib import EmbedMaker
import re
import asyncio
import discord
unit_compiled = re.compile(r"^[a-z\-_]+$")


class CryptoCreateController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = CryptoModel()

    @commands.command(aliases=['register'])
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def create(self, ctx: commands.Context, name: str, unit: str) -> None:
        """
        新しい通貨を発行します。一つのサーバーにつき一通貨までしか発行できません。
        引数の詳細:
            name: 通貨の名前です。例: DiscordMoney
            unit: 通貨の単位です。英字、アンダースコア、横棒が使えます。例: dm
        """
        if await self.model.guild_exists(ctx.guild.id):
            await EmbedMaker(ctx).by_error_text("このサーバーではすでに通貨が作成されています。").send()
            return

        if await self.model.name_exists(name):
            await EmbedMaker(ctx).by_error_text("その名前の通貨はすでに存在します。").send()
            return

        if await self.model.unit_exists(unit):
            await EmbedMaker(ctx).by_error_text("その単位の通貨はすでに存在します。").send()
            return

        if unit_compiled.match(unit) is None:
            await EmbedMaker(ctx).by_error_text("その単位の表記は使用できません。他の表記に変更してください。英大文字は使用できません。").send()
            return

        embed = discord.Embed(
            title="確認",
            description=f"通貨名: {name}, 単位: `{unit}` "
                        f"で通貨を作成しますか?\n作成する場合は`accept`, キャンセルする場合は他の文字を打ってください。")
        await EmbedMaker(ctx).default(embed).send()

        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            return

        if msg.content != "accept":
            await EmbedMaker(ctx).by_error_text("通貨の作成をキャンセルしました。").send()
            return

        await EmbedMaker(ctx).success(discord.Embed(title="作成開始", description="通貨を作成します...")).send()
        r = await self.model.create(
            guild_id=ctx.guild.id,
            name=name,
            unit=unit,
            member_count=ctx.guild.member_count
        )
        if r:
            await EmbedMaker(ctx)\
                .by_success_text(f"通貨の作成が完了しました。\n`vc.info {unit}`コマンドか、このサーバー内で`vc.info`コマンドを使用して確認してください。").send()
            return
        await EmbedMaker(ctx).by_error_text("不明なエラーが発生しました。").send()

    @create.error
    async def create_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.BadArgument):
            return
        if ctx.guild is None:
            await EmbedMaker(ctx).by_error_text("このコマンドはサーバー専用です。").send()
            return
        if not ctx.author.guild_permissions.administrator:
            await EmbedMaker(ctx).by_error_text("このコマンドを実行する権限がありません。(必要な権限: 管理者)").send()
        raise exception


def setup(bot):
    return bot.add_cog(CryptoCreateController(bot))
