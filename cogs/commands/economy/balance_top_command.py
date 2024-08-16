import discord
from discord.ext import commands
from discord import app_commands
import asyncio

from main import config
from database.models import EconomyUser

class balance_top_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="balance-top", description="Zeigt die 10 reichsten Mitglieder an")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def balance_top(self, interaction: discord.Interaction):
        await interaction.response.defer()
        economy_user = await EconomyUser(interaction.user.id).load()
        top_raw = await economy_user.get_top_users()
        
        user_list = ""
        pos = 1  
        for u in top_raw:
            user: discord.User = self.client.get_user(u[0])
            if user:
                if u[1] >= 10000:
                    coins = f"{u[1] // 1000}k"
                elif u[1] >= 1000:
                    coins = f"{(u[1] / 1000):.1f}k"
                else:
                    coins = u[1]

                user_list += f"**#{pos}** • {user.name} • {coins} 🪙\n"
            else:
                user_list += f"**#{pos}** • `Null` • {coins} 🪙\n"
            pos += 1
        embed = discord.Embed(title="Economy Leaderboard", description=user_list, color=0xa7acb4)
        embed.set_thumbnail(url=interaction.guild.icon.url)
        await interaction.edit_original_response(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(balance_top_command(client))