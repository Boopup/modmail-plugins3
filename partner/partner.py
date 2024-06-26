import discord
from discord.ext import commands
from discord import app_commands

class Affiliate(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def announce(self, ctx):
        role_id = 1158167769523687494
        channel_id = 1003340995980705952

        # Check if the user has the required role
        if role_id not in [role.id for role in ctx.author.roles]:
            await ctx.send("Yikes! You don't have the required role - Talk to a representative if you believe you should be able to do this action.")
            return

        # Create an embed with a button to open the form
        embed = discord.Embed(
            title="Announcement Menu",
            description="Click the button below to submit an announcement.",
            color=discord.Color.blue()  # Use bot's main color
        )
        
        view = discord.ui.View()
        button = discord.ui.Button(label="Submit Announcement", style=discord.ButtonStyle.primary)

        async def button_callback(interaction):
            modal = AnnouncementForm(bot=self.bot, channel_id=channel_id)
            await interaction.response.send_modal(modal)

        button.callback = button_callback
        view.add_item(button)

        await ctx.send(embed=embed, view=view)

class AnnouncementForm(discord.ui.Modal):
    def __init__(self, bot, channel_id):
        super().__init__(title="Announcement Form")
        self.bot = bot
        self.channel_id = channel_id

        self.group = discord.ui.TextInput(label="Group", style=discord.TextStyle.short)
        self.announcement = discord.ui.TextInput(label="Announcement", style=discord.TextStyle.long)
        
        self.add_item(self.group)
        self.add_item(self.announcement)

    async def on_submit(self, interaction):
        group = self.group.value
        announcement = self.announcement.value

        embed = discord.Embed(
            title=f"Announcement from {group}",
            description=announcement,
            color=discord.Color.blue()  # Use bot's main color
        )
        
        channel = self.bot.get_channel(self.channel_id)
        await channel.send(embed=embed)
        await interaction.response.send_message("Your announcement has been posted!", ephemeral=True)

async def setup(bot):
    await bot.add_cog(Affiliate(bot))
