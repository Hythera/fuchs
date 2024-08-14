import discord
from discord.ext import commands
from discord import app_commands
import json

from main import config
from cogs.channel_system import VoiceButtons

with open("json/list_images.json", 'r', encoding='utf-8') as file:
    images = json.load(file)

class setup_interface_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="setup-interface", description="Erlaubt es dir das Interface in diesem Kanal zu erstellen")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    @app_commands.default_permissions(administrator=True)
    async def setup_interface(self, interaction: discord.Interaction):
        channel = interaction.channel
        embed = discord.Embed(title="Voice Interface", description="Mit diesem **Interface** kannst du deinen temporären Kanal bearbeiten.", color=0x6d6f78)
        embed.set_image(url=images["interface_card"])
        await interaction.response.send_message("✅ Interface Embed erfolgreich gesendet.", ephemeral=True)
        await channel.send(embed=embed, view=VoiceButtons(client=self.client))

async def setup(client:commands.Bot) -> None:
    await client.add_cog(setup_interface_command(client))