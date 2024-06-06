import discord
from discord.ext import commands
import aiohttp

class WhoisPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="whois")
    async def whois_user(self, ctx, *, username):
        # Step 1: Call Roblox API's search endpoint to find the user ID
        async with aiohttp.ClientSession() as session:
            search_url = f"https://users.roblox.com/v1/users/search?keyword={username}&limit=10"
            async with session.get(search_url) as response:
                if response.status != 200:
                    await ctx.send("Failed to retrieve data from Roblox API.")
                    return
                search_data = await response.json()
                if not search_data["data"]:
                    await ctx.send("User not found on Roblox.")
                    return

                # Get the top 3 search results
                top_results = search_data["data"][:3]

        # Step 2: Create embeds for each user
        for user_data in top_results:
            user_id = user_data["id"]

            # Retrieve the user's profile information
            async with aiohttp.ClientSession() as session:
                user_url = f"https://users.roblox.com/v1/users/{user_id}"
                async with session.get(user_url) as response:
                    if response.status != 200:
                        await ctx.send("Failed to retrieve user profile from Roblox API.")
                        return
                    user_profile = await response.json()

            # Construct the embed
            embed = discord.Embed(
                title=f"{user_profile['name']}'s Profile",
                description=f"```{user_profile['description']}```",
                color=discord.Color.blue()
            )
            embed.add_field(name="Created", value=user_profile["created"], inline=False)

            # Send the embed
            await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WhoisPlugin(bot))
