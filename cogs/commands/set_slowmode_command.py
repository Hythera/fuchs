import discord
from discord.ext import commands
from discord import app_commands

from main import config

class set_slowmode_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="set-slowmode", description="Setze einen custom slowmode")
    @app_commands.describe(seconds="Die Sekundenanzahl des Slowmodes")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    @app_commands.default_permissions(administrator=True)
    async def set_slowmode(self, interaction: discord.Interaction, seconds: int):
        seconds = abs(seconds)
        await interaction.channel.edit(slowmode_delay=seconds)
        await interaction.response.send_message(f"✅ Slowmode erfolgreich auf `{seconds}` Sekunden gesetzt.", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(set_slowmode_command(client))