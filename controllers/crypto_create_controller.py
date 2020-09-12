from models import CryptoModel
from discord.ext import commands
import asyncio


class CryptoCreateController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = CryptoModel()

    @commands.command(aliases=['register'])
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def create(self, ctx: commands.Context, name: str, unit: str) -> None:
        if await self.model.guild_exists(ctx.guild.id):
            await ctx.send("このサーバーではすでに通貨が作成されています。")
            return

        if await self.model.name_exists(name):
            await ctx.send("その名前の通貨はすでに存在します。")
            return

        if await self.model.unit_exists(unit):
            await ctx.send("その単位の通貨はすでに存在します。")
            return

        await ctx.send(f"通貨名: {name}, 単位: {unit}で通貨を作成しますか?\n作成する場合は`accept`, キャンセルする場合は他の文字を打ってください。")

        def check(m):
            return m.channel.id == ctx.channel.id and m.author.id == ctx.author.id

        try:
            msg = await self.bot.wait_for("message", check=check, timeout=60)
        except asyncio.TimeoutError:
            return

        if msg.content != "accept":
            await ctx.send("通貨の作成をキャンセルしました。")
            return

        await ctx.send("通貨を作成します...")
        await self.model.create(
            guild_id=ctx.guild.id,
            name=name,
            unit=unit
        )
        await ctx.send(f"通貨の作成が完了しました。\n`vc.info {unit}`コマンドか、`vc.guild`コマンドで確認してください。")
        return

    @create.error
    async def create_error(self, ctx: commands.Context, exception):
        if isinstance(exception, commands.BadArgument):
            return
        if ctx.guild is None:
            await ctx.send("このコマンドはギルド専用です。")
            return
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("このコマンドを実行する権限がありません。(必要な権限: 管理者)")


def setup(bot):
    return bot.add_cog(CryptoCreateController(bot))
