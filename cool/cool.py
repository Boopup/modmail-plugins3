import discord
from discord.ext import commands
import aiohttp

class ActivityPlugin(commands.Cog):
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

    @commands.command(name="activitystats")
    async def activity_stats(self, ctx, username: str = None):
        bloxlink_api_key = "c55318be-bd8d-4886-aaa2-7052a81021ea"
        easypos_token = "e084ca0f-e604-4568-ad73-fea11b9fee20"

        if username:
            # Step 1: Get Roblox user ID from the provided username
            roblox_user_id = await self.get_user_id(username)
            if not roblox_user_id:
                await ctx.send(f"User '{username}' not found or is banned on Roblox.")
                return
        else:
            # Step 1: Get Roblox user ID from Bloxlink for the command invoker
            server_id = ctx.guild.id
            user_id = ctx.author.id

            async with aiohttp.ClientSession() as session:
                async with session.get(f"https://api.blox.link/v4/public/guilds/{server_id}/discord-to-roblox/{user_id}", headers={"Authorization": bloxlink_api_key}) as response:
                    if response.status != 200:
                        await ctx.send("Failed to retrieve data from Bloxlink API.")
                        return
                    bloxlink_data = await response.json()
                    print(f"Bloxlink API Response: {bloxlink_data}")  # Debugging line
                    roblox_user_id = bloxlink_data.get("robloxID")
                    if not roblox_user_id:
                        await ctx.send("Roblox user ID not found in BloxLink, not sure how you're using this...")
                        return

        # Step 2: Call EasyPOS API to get activity data
        async with aiohttp.ClientSession() as session:
            async with session.post("https://papi.easypos.lol/activity", json={"token": easypos_token, "userId": roblox_user_id}) as response:
                if response.status != 200:
                    await ctx.send("Failed to retrieve data from EasyPOS API.")
                    return
                easypos_data = await response.json()

        # Extract data from EasyPOS response
        total_playtime = easypos_data["total_playtime"]
        total_formatted = easypos_data["total_formatted"]
        average_formatted = easypos_data["average_formatted"]
        position = easypos_data["position"]

        # Step 3: Send the embed with activity data
        embed = discord.Embed(
            title="🕛 Activity",
            description=(
                f"<@{user_id}>'s Activity** \n\n"
                f"Your total playtime is: **{total_formatted}** \n\n"
                f"Your Daily average is: **{average_formatted}**!\n\n"
                f"Your position on the leaderboard is: #{position} \n\n"
            ),
            color=discord.Color.blue()
        )

        # Add user avatar
        embed.set_thumbnail(url=f"https://roblox-avatar.eryn.io/{roblox_user_id}?format=webp")

        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(ActivityPlugin(bot))
