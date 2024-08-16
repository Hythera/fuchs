import discord
from discord.ext import commands
from discord import app_commands
import random

from database.models import EconomyUser
from main import config

class work_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="work", description="Arbeite für etwas extra Coins")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    @app_commands.checks.cooldown(1, 3600, key=lambda interaction: (interaction.guild_id, interaction.user.id))
    async def work(self, interaction: discord.Interaction):
        economy_user = await EconomyUser(interaction.user.id).load()
        coins = int(random.randint(100,200)*economy_user.multiplier)
        await economy_user.add_data(coins=coins)
        await interaction.response.send_message(f"✅ Du hast etwas gearbeitet und {coins} 🪙 bekommen")

async def setup(client:commands.Bot) -> None:
    await client.add_cog(work_command(client))