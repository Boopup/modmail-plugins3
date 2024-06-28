# customstatus.py

import discord
from discord.ext import commands, tasks
import random

class CustomStatus(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.statuses = [
            "🔎 Overseeing Tickets",
            "📨 DM to create a ticket!",
            "🏨 Watching Coral Coast Hotels",
            "💪 Coastie for the win!"
        ]
        self.status_task = None

    def cog_unload(self):
        if self.status_task:
            self.status_task.cancel()

    async def set_status(self, status):
        await self.bot.change_presence(activity=discord.CustomActivity(name=status))

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.status_task:
            self.status_task = self.rotate_status.start()

    @tasks.loop(seconds=30.0)
    async def rotate_status(self):
        status = discord.CustomActivity(name=random.choice(self.statuses))
        await self.bot.change_presence(activity=status)

    @rotate_status.before_loop
    async def before_rotate_status(self):
        await self.bot.wait_until_ready()

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def customactivityon(self, ctx):
        if self.status_task and not self.status_task.is_running():
            self.status_task.start()
            await ctx.send("Status rotation has been enabled.")
        elif not self.status_task:
            self.status_task = self.rotate_status.start()
            await ctx.send("Status rotation has been enabled.")
        else:
            await ctx.send("Status rotation is already enabled.")

    @customactivityon.error
    async def customactivityon_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("You do not have permission to use this command.")

async def setup(bot):
   await bot.add_cog(CustomStatus(bot))
