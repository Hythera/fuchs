import discord
from discord.ext import commands
from discord import app_commands

from database.models import EconomyUser
from main import config

class balance_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="balance", description="Zeigt dir deinen aktuellen Coin-Stand")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    @app_commands.default_permissions(administrator=True)
    async def setup_interface(self, interaction: discord.Interaction, member: discord.Member = None):
        if member: 
            if member.bot:
                await interaction.response.send_message("❌ Du kannst das Level von APPs nicht einsehen.", ephemeral=True)
                return
            else:
                user = member
        else:
            user = interaction.user
        economy_user = await EconomyUser(user.id).load()
        await interaction.response.send_message(f"{economy_user.coins} - {economy_user.multiplier}", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(balance_command(client))