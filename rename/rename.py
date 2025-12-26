import discord
from discord.ext import commands
from core import checks
from core.models import PermissionLevel
import datetime

class Rename(commands.Cog):
    """Rename a thread!"""
    def __init__(self, bot):
        self.bot = bot
    
    @checks.thread_only()
    @checks.has_permissions(PermissionLevel.SUPPORTER)
    @commands.command()
    async def rename(self, ctx, *, request):
        try:
            await ctx.message.add_reaction('⏰')
            
            # Get the thread and its recipient (the person who opened the ticket)
            thread = ctx.thread
            recipient = thread.recipient
            
            nickname = recipient.display_name if recipient else "Unknown"
            
            new_name = request.replace("!NICKNAME!", nickname)
            
            await ctx.channel.edit(name=new_name)
            
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('✅')
        except discord.errors.Forbidden:
            embed = discord.Embed(
                title='Forbidden',
                description="Uh oh, it seems I can't perform this action due to my permission levels.",
                color=discord.Color.red()
            )
            embed.timestamp = datetime.datetime.utcnow()
            embed.set_footer(text='Rename')
            await ctx.reply(embed=embed)
            
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('❌')
        except:
            await ctx.message.clear_reactions()
            await ctx.message.add_reaction('❌')

async def setup(bot):
    await bot.add_cog(Rename(bot))
