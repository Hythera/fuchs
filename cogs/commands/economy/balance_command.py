import discord
from discord.ext import commands
from discord import app_commands
import json

from database.models import EconomyUser
from main import config

with open("json/list_images.json", 'r', encoding='utf-8') as file:
    images = json.load(file)

class balance_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="balance", description="Zeigt dir deinen aktuellen Coin-Stand")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def balance(self, interaction: discord.Interaction, member: discord.Member = None):
        if member: 
            if member.bot:
                await interaction.response.send_message("❌ Du kannst den Kontostand von APPs nicht einsehen.", ephemeral=True)
                return
            else:
                user = member
        else:
            user = interaction.user
        economy_user = await EconomyUser(user.id).load()
        embed = discord.Embed(color=0xa7acb4)

        if user.avatar:
            embed.set_author(icon_url=user.avatar.url, name=user.name)
        else:
            embed.set_author(icon_url=images["standard_profile_picture"], name=user.name)
        embed.add_field(name="Coins", value=f"{economy_user.coins} 🪙", inline=True)
        embed.add_field(name="Bank", value=f"{economy_user.bank} 🪙", inline=True)
        embed.add_field(name="Gesamt", value=f"{economy_user.coins + economy_user.bank} 🪙", inline=True)
        await interaction.response.send_message(embed=embed)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(balance_command(client))