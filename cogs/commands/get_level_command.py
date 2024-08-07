import discord
from discord.ext import commands
from discord import app_commands

from database.models import LevelUser
from main import config

from easy_pil import Editor, Canvas, Font, load_image

async def generate_card(user: discord.User, xp, xp_next, level, position):
    background = Editor("images/level_background.png")

    profile_picture = load_image(str(user.avatar.url))
    profile = Editor(profile_picture).resize((150, 150)).circle_image()

    poppins = Font.poppins(size=40)
    poppins_small = Font.poppins(size=30)
    poppins_huge = Font.poppins(size=100)

    background.paste(profile, (30, 30))

    background.rectangle((30, 220), width=830, height=40, color="#282828", radius=20)
    background.bar((30, 220), max_width=830, height=40, percentage=int((xp/xp_next)*100), color="#414141", radius=20)

    background.text((200, 40), user.name, font=poppins, color="#282828")
    background.rectangle((200, 100), width=350, height=2, fill="#282828")
    background.text((200, 130), f"Level {level}    {xp}XP / {xp_next}XP", font=poppins_small, color="#282828")


    if len(position) == 1:
        xpos = 700
    elif len(position) == 2:
        xpos = 650
    else:
        xpos= 600
    background.text((xpos, 100), f"#{position}", font=poppins_huge, color="#282828")

    return discord.File(fp=background.image_bytes, filename="levelcard.png")

class get_level_command(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @app_commands.command(name="level", description="Zeigt dir dein Level oder das von jeman anderem an")
    @app_commands.describe(member="Gib einen Nutzer an")
    @app_commands.guild_only()
    @app_commands.guilds(int(config["guild_id"]))
    async def level(self, interaction: discord.Interaction, member: discord.Member = None):
        if member: 
            if member.bot:
                await interaction.response.send_message("❌ Du kannst das Level von APPs nicht einsehen.", ephemeral=True)
                return
            else:
                user = member
        else:
            user = interaction.user
        await interaction.response.defer()
        level_user = await LevelUser(user.id).load()
        file = await generate_card(user, level_user.xp, level_user.get_xp_for_next_level(), level_user.get_level(), str(await level_user.get_position()))
        await interaction.edit_original_response(attachments=[file])

async def setup(client:commands.Bot) -> None:
    await client.add_cog(get_level_command(client))