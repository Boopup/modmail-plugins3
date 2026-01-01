import discord
from discord.ext import commands
import datetime
import urllib.parse

class Boogle(commands.Cog):
    """Generate a Boogle search link"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def boogle(self, ctx, *, text: str):
        query = urllib.parse.quote_plus(text)
        url = f"https://boopup.dev/search?q={query}"

        embed = discord.Embed(
            title="Your Boogle Search is ready.",
            description=(
                "Here's your Boogle Search to save yourself time. :) "
                "Copy this link or forward this to them.\n\n"
                f"{url}"
            ),
        )
        embed.timestamp = datetime.datetime.utcnow()

        await ctx.reply(embed=embed)

async def setup(bot):
    await bot.add_cog(Boogle(bot))
