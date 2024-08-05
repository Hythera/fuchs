import discord
from discord.ext import commands

from main import config

class join_role(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client

    @commands.Cog.listener("on_member_join")
    async def on_member_join(self, member: discord.Member):
        role = member.guild.get_role(config["join_role"])
        await member.add_roles(role)

async def setup(client:commands.Bot) -> None:
    await client.add_cog(join_role(client))