import discord
from discord.ext import commands
import aiohttp

class WhoisPlugin(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_user_id(self, name):
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://users.roblox.com/v1/usernames/users'
                payload = {
                    "usernames": [name],
                    "excludeBannedUsers": True
                }
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        return None
                    data = await response.json()
                    if not data["data"]:
                        return None
                    return data["data"][0]["id"]
        except Exception as e:
            print(f"Error fetching user ID: {e}")
            return None

    @commands.command(name="whois")
    async def whois_user(self, ctx, *, username):
        # Step 1: Get Roblox user ID from username
        user_id = await self.get_user_id(username)
        if not user_id:
            await ctx.send(f"User '{username}' not found or is banned on Roblox.")
            return

        # Step 2: Retrieve the user's profile information
        async with aiohttp.ClientSession() as session:
            user_url = f"https://users.roblox.com/v1/users/{user_id}"
            async with session.get(user_url) as response:
                if response.status != 200:
                    await ctx.send("Failed to retrieve user profile from Roblox API.")
                    return
                user_profile = await response.json()

        # Step 3: Construct the embed
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
