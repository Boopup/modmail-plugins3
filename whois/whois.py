import discord
from discord.ext import commands
import aiohttp

class RobloxCommands(commands.Cog, name="Roblox Commands"):
    def __init__(self, bot):
        self.bot = bot

    async def get_roblox_user_id(self, username):
        try:
            async with aiohttp.ClientSession() as session:
                url = 'https://users.roblox.com/v1/usernames/users'
                payload = {
                    "usernames": [username],
                    "excludeBannedUsers": True
                }
                async with session.post(url, json=payload) as response:
                    if response.status != 200:
                        return None, None
                    data = await response.json()
                    if data['data']:
                        return data['data'][0]['id'], data['data'][0]['name']
                    else:
                        return None, None
        except Exception as e:
            print(f"Error fetching Roblox user ID: {e}")
            return None, None

    async def fetch_user_headshot(self, user_id):
        async with aiohttp.ClientSession() as session:
            url = f'https://thumbnails.roblox.com/v1/users/avatar-headshot?userIds={user_id}&size=100x100&format=Png&isCircular=true'
            async with session.get(url) as response:
                if response.status != 200:
                    return None
                data = await response.json()
                return data['data'][0]['imageUrl'] if 'data' in data and len(data['data']) > 0 else None

    @commands.command(name="whois", help="Find information about a Roblox user")
    async def whois(self, ctx, username: str):
        user_id, roblox_username = await self.get_roblox_user_id(username)
        if not user_id:
            await ctx.send(f"Failed to retrieve Roblox user ID for username '{username}'.")
            return

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://users.roblox.com/v1/users/{user_id}") as response:
                if response.status != 200:
                    await ctx.send("Failed to retrieve data from Roblox API.")
                    return
                user_data = await response.json()

        description = user_data.get("description", "Nothing is currently in this user's description.")
        created = user_data.get("created", "Unknown")
        display_name = user_data.get("displayName", roblox_username)
        is_verified = user_data.get("hasVerifiedBadge", False)
        verified_emoji = "<:_:1066389333025751080>" if is_verified else ""

        headshot_url = await self.fetch_user_headshot(user_id)

        embed = discord.Embed(
            title=f"{verified_emoji} {roblox_username}'s Profile",
            description=f"> **Description:**\n```\n{description}\n```\n",
            url=f"https://www.roblox.com/users/{user_id}/profile",
            color=discord.Color.blue()
        )

        if headshot_url:
            embed.set_thumbnail(url=headshot_url)

        embed.add_field(name="User ID", value=user_id, inline=False)
        embed.add_field(name="Display Name", value=display_name, inline=False)
        embed.add_field(name="Created", value=created, inline=False)

        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/followers/count") as response:
                if response.status == 200:
                    followers_data = await response.json()
                    embed.add_field(name="Followers", value=followers_data.get("count", "N/A"), inline=True)

            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/followings/count") as response:
                if response.status == 200:
                    followings_data = await response.json()
                    embed.add_field(name="Following", value=followings_data.get("count", "N/A"), inline=True)

            async with session.get(f"https://friends.roblox.com/v1/users/{user_id}/friends/count") as response:
                if response.status == 200:
                    friends_data = await response.json()
                    embed.add_field(name="Friends", value=friends_data.get("count", "N/A"), inline=True)

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(RobloxCommands(bot))
