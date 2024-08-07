
import discord
from discord.ext import commands
from discord import app_commands

from main import config
from database.models import LevelUser

class leaderboard_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="leaderboard", description="Zeigt die Top 10 Nutzer an")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def leaderboard(self, interaction: discord.Interaction):
        level_user = await LevelUser(interaction.user.id).load()
        top_raw = await level_user.get_top_users()
        
        top_users = {}
        user_list = ""
        pos = 1  
        for u in top_raw:
            user: discord.User = await self.client.fetch_user(u[0])
            top_users[u[0]] = [user.name, u[1]]
            user_list += f"**#{pos}** • {user.name} • {int((u[1] / 50) ** (1 / 1.5))}\n"
            pos += 1
        embed = discord.Embed(title="Level Leaderboard", description=user_list, color=0xa7acb4)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(leaderboard_command(client))