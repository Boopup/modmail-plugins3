import discord
from discord.ext import commands

class CustomActivity(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='customactivity')
    @commands.has_permissions(administrator=True)
    async def set_custom_activity(self, ctx, activity_name: str):
        try:
            # Ensure emoji is correctly formatted with Unicode
            emoji = f'{emoji.strip()}'
            activity = discord.CustomActivity(name=activity_name)
            await self.bot.change_presence(activity=activity)
            await ctx.send(f'Set custom activity to {activity_name}')
        except Exception as e:
            await ctx.send(f'Error setting custom activity: {e}')

    @set_custom_activity.error
    async def custom_activity_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You need to be an administrator to use this command.")

async def setup(bot):
    await bot.add_cog(CustomActivity(bot))
