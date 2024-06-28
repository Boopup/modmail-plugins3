import discord
from discord.ext import commands

class CustomActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='customactivity')
    @commands.has_permissions(administrator=True)
    async def set_custom_activity(self, ctx, emoji: str, *, activity_name: str):
        try:
            activity = discord.CustomActivity(name=activity_name, emoji=emoji)
            await self.bot.change_presence(activity=activity)
            await ctx.send(f'Set custom activity to {emoji} {activity_name}')
        except Exception as e:
            await ctx.send(f'Error setting custom activity: {e}')

    @set_custom_activity.error
    async def custom_activity_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need to be an administrator to use this command.")

async def setup(bot):
    await bot.add_cog(CustomActivity(bot))
