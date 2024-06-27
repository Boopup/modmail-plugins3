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
                self.register_as_slash(command)

        # Add the command group to the bot
        self.bot.add_application_command(self.command_group)

    def register_as_slash(self, command):
        @self.command_group.command(name=command.name, description=command.help or "No description provided.")
        async def _slash_command(ctx: discord.ApplicationContext, *args):
            await ctx.defer()
            # Create a fake context to pass to the original command
            fake_ctx = await self.bot.get_context(ctx.interaction)
            fake_ctx.command = command
            fake_ctx.interaction = ctx.interaction  # Attach the interaction to the context
            await command.callback(fake_ctx, *args)

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"AutoSlashCommands cog loaded. {len(self.command_group.subcommands)} slash commands registered.")

async def setup(bot):
    await bot.add_cog(AutoSlashCommands(bot))
