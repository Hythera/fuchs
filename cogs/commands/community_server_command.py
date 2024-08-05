import discord
from discord.ext import commands
from discord import app_commands
import json

from main import config

def save_to_json(location, content):
    with open(location, 'w') as file:
        json.dump(content, file, indent=4)

class community_server_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="community-server-status", description="Setze den Status des Community-Servers")
    @app_commands.describe(status="Status des Community-Servers")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    @app_commands.default_permissions(administrator=True)
    @app_commands.choices(status=[app_commands.Choice(name="An", value="True"), app_commands.Choice(name="Aus", value="False")])
    async def test(self, interaction: discord.Interaction, status: app_commands.Choice[str]):
        self.client.storage["community_server_status"] = status.value
        save_to_json("json/data.json", self.client.storage)
        await interaction.response.send_message(f"✅ Status auf `{status.name}` gesetzt.", ephemeral=True)


async def setup(client:commands.Bot) -> None:
    await client.add_cog(community_server_command(client))