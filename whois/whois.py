import discord
from discord.ext import commands
import aiohttp
from datetime import datetime

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

    async def get_following_count(self, user_id):
        async with aiohttp.ClientSession() as session:
            url = f"https://friends.roblox.com/v1/users/{user_id}/followings/count"
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data.get("count", 0)

    async def get_followers_count(self, user_id):
        async with aiohttp.ClientSession() as session:
            url = f"https://friends.roblox.com/v1/users/{user_id}/followers/count"
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data.get("count", 0)

    async def get_friends_count(self, user_id):
        async with aiohttp.ClientSession() as session:
            url = f"https://friends.roblox.com/v1/users/{user_id}/friends/count"
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data.get("count", 0)

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

        # Step 3: Get followers, following, and friends counts
        following_count = await self.get_following_count(user_id)
        followers_count = await self.get_followers_count(user_id)
        friends_count = await self.get_friends_count(user_id)

        # Step 4: Construct the embed
        description = user_profile["description"] or "Nothing is currently in this user's description."
        created_at = datetime.fromisoformat(user_profile["created"].replace('Z', '+00:00'))
        verified = user_profile.get("hasVerifiedBadge", False)
        title_prefix = "<:_:1066389333025751080> " if verified else ""

        embed = discord.Embed(
            title=f"{title_prefix}{user_profile['name']}'s Profile",
            url=f"https://www.roblox.com/users/{user_id}/profile",
            description=f"```{description}```",
            color=discord.Color.blue()
        )
        embed.add_field(name="Display Name", value=user_profile.get("displayName", "N/A"), inline=False)
        embed.add_field(name="User ID", value=user_id, inline=False)
        embed.add_field(name="Created", value=created_at.strftime('%Y-%m-%d %H:%M:%S'), inline=False)
        embed.add_field(name="Following", value=following_count, inline=True)
        embed.add_field(name="Followers", value=followers_count, inline=True)
        embed.add_field(name="Friends", value=friends_count, inline=True)
        embed.set_thumbnail(url=f"https://roblox-avatar.eryn.io/{user_id}?format=webp")

        # Send the embed
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(WhoisPlugin(bot))
