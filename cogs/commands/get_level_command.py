import discord
from discord.ext import commands
from discord import app_commands

from database.models import LevelUser
from main import config

from PIL import Image, ImageDraw, ImageFont
import io

class get_level_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="level", description="Zeigt dir dein Level an")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def add_global(self, interaction: discord.Interaction):
        level_user = await LevelUser(interaction.user.id).load()
        level = level_user.get_level()
        xp = level_user.xp
        messages = level_user.messages
        

        await interaction.response.send_message(f"Level: {level}, XP: {xp}, Messages: {messages}", ephemeral=True)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(get_level_command(client))