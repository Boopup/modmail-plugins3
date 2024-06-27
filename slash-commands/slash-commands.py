import discord
from discord.ext import commands
from discord.commands import SlashCommandGroup

class AutoSlashCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.command_group = SlashCommandGroup("commands", "Auto-generated slash commands")

    async def cog_load(self):
        # Register all existing commands as slash commands
        for command in self.bot.commands:
            if not command.hidden:  # Skip hidden commands
                await self.register_as_slash(command)

        # Add the command group to the bot
        self.bot.tree.add_command(self.command_group)
        await self.bot.tree.sync()

    async def register_as_slash(self, command):
        @self.command_group.command(name=command.name, description=command.help or "No description provided.")
        async def _slash_command(interaction: discord.Interaction, *args):
            await interaction.response.defer()
            # Create a fake context to pass to the original command
            fake_ctx = await self.bot.get_context(interaction)
            fake_ctx.command = command
            await command.callback(fake_ctx, *args)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"AutoSlashCommands cog loaded. {len(self.command_group.subcommands)} slash commands registered.")

async def setup(bot):
    await bot.add_cog(AutoSlashCommands(bot))
