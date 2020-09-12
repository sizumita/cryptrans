from models import CryptoModel
from discord.ext import commands
import re
import asyncio
unit_compiled = re.compile(r"^[A-Za-z\-_]+$")


class CryptoCreateController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.model = CryptoModel()

    @commands.command(aliases=['register'])
    @commands.has_guild_permissions(administrator=True)
    @commands.guild_only()
    async def create(self, ctx: commands.Context, name: str, unit: str, per_amount: int) -> None:
        """
        新しい通貨を発行します。一つのサーバーにつき一通貨までしか発行できません。
        引数の詳細:
            name: 通貨の名前です。例: DiscordMoney
            unit: 通貨の単位です。英字、アンダースコア、横棒が使えます。例: dm
            per_amount: 通貨が10分ごと何枚増えるかを入力します。例えば100枚であれば１日に144,000枚増える計算になります。例: 100
        """
        if await self.model.guild_exists(ctx.guild.id):
            await ctx.send("このサーバーではすでに通貨が作成されています。")
            return

        if await self.model.name_exists(name):
            await ctx.send("その名前の通貨はすでに存在します。")
            return

        if await self.model.unit_exists(unit):
            await ctx.send("その単位の通貨はすでに存在します。")
            return

        if unit_compiled.match(unit) is None:
            await ctx.send("その単位の表記は使用できません。他の表記に変更してください。")
            return

        await ctx.send(f"通貨名: {name}, 単位: {unit}, 10分ごとの増加量: {per_amount}{unit} "
                       f"で通貨を作成しますか?\n作成する場合は`accept`, キャンセルする場合は他の文字を打ってください。")

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
        r = await self.model.create(
            guild_id=ctx.guild.id,
            name=name,
            unit=unit,
            per_amount=per_amount
        )
        if r:
            await ctx.send(f"通貨の作成が完了しました。\n`vc.info {unit}`コマンドか、このサーバー内で`vc.info`コマンドを使用して確認してください。")
            return
        await ctx.send("不明なエラーが発生しました。")

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
