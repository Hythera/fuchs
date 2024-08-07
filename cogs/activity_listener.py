import discord
from discord.ext import commands
import datetime
import asyncio

from main import config
from database.models import LevelUser

async def send_level_up(member: discord.Member, level_user: LevelUser, channel: discord.abc.Messageable):
    message = await channel.send(content=f"{member.mention} ist nun Level **{level_user.get_data()[0]}**!")
    await asyncio.sleep(10)
    await message.delete()

class activity_listener(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.last_activities = {}

    @commands.Cog.listener("on_message")
    async def on_message(self, message: discord.Message):
        if message.author.bot:
            return
        
        if message.author.id in self.last_activities:
            if self.last_activities[message.author.id] + datetime.timedelta(seconds=15) > message.created_at:
                return
        
        level_user = await LevelUser(message.author.id).load()

        if await level_user.add_data(1,1):
            await send_level_up(message.author, level_user, message.channel)

        self.last_activities[message.author.id] = message.create_at

async def setup(client:commands.Bot) -> None:
    await client.add_cog(activity_listener(client))