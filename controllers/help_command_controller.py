from discord.ext import commands
import discord
from lib import EmbedMaker


class HelpCommandController(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.help_embed = discord.Embed(
            title="virtualCrypto Help",
        )
        self.help_embed.add_field(
            name="コマンド一覧",
            value="[公式Wikiコマンド一覧ページ](https://github.com/virtualCrypto-discord/virtualCrypto/wiki/Commands)",
            inline=False
        )
        self.help_embed.add_field(
            name="各種URL",
            value="[公式サーバー](https://discord.gg/Hgp5DpG)\n"
                  "[Botの招待](https://discord.com/api/oauth2/authorize?client_id=754196279315398666&permissions=912448&scope=bot)\n"
                  "[公式Wiki](https://github.com/virtualCrypto-discord/virtualCrypto/wiki)",
            inline=False
        )

    @commands.command()
    async def help(self, ctx: commands.Context):
        await EmbedMaker(ctx).default(self.help_embed).send()


def setup(bot):
    return bot.add_cog(HelpCommandController(bot))
