import discord
from discord.ext import commands

class AutoSlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def cog_load(self):
        # Register all existing commands as slash commands
        for command in self.bot.commands:
            if not command.hidden:  # Skip hidden commands
                await self.register_as_slash(command)

        # Sync the command tree to ensure all commands are registered
        await self.bot.tree.sync()

    async def register_as_slash(self, command: commands.Command):
        async def _slash_command(interaction: discord.Interaction, *args: str):
            await interaction.response.defer()
            # Create a fake context to pass to the original command
            fake_ctx = await self.bot.get_context(interaction)
            fake_ctx.command = command
            await command.callback(fake_ctx, *args)
        
        # Create a new command for each existing command
        new_command = discord.app_commands.Command(
            name=command.name,
            description=command.help or "No description provided.",
            callback=_slash_command,
        )
        
        # Add the new command to the bot's tree
        self.bot.tree.add_command(new_command)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"AutoSlashCommands cog loaded.")

async def setup(bot):
    await bot.add_cog(AutoSlashCommands(bot))
