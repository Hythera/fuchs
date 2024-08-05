import os
from dotenv import load_dotenv
import json
from pathlib import Path

import discord
from discord.ext import commands

import time
from colorama import Fore, Back, Style
import platform

from cogs import ticket_system
from cogs import channel_system

load_dotenv()
with open("config.json", 'r', encoding='utf-8') as file:
    config = json.load(file)
with open("json/data.json", 'r', encoding='utf-8') as file:
    storage = json.load(file)


if not os.path.exists("json"):
    os.makedirs("json")
if not os.path.exists("json/data.json"):
    with open("json/data.json", 'w', encoding='utf-8') as file:
        json.dump({"community_server_status": "False","counting_current_number": 2,"counting_last_user": 1204122491929366558}, file, ensure_ascii=False, indent=4)
if not os.path.exists("json/tickets.json"):
    with open("json/tickets.json", 'w', encoding='utf-8') as file:
        json.dump({}, file, ensure_ascii=False, indent=4)
if not os.path.exists("json/list_emoji.json"):
    with open("json/list_emoji.json", 'w', encoding='utf-8') as file:
        json.dump({}, file, ensure_ascii=False, indent=4)
if not os.path.exists("json/list_images.json"):
    with open("json/list_images.json", 'w', encoding='utf-8') as file:
        json.dump({}, file, ensure_ascii=False, indent=4)

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.all()
        super().__init__(command_prefix='/syntheria', intents=intents)
        
        self.cogslist = ['.'.join(file.relative_to('cogs').with_suffix('').parts) for file in Path('cogs').rglob('*.py') if not file.name.startswith('__')]

        self.storage = storage


    async def setup_hook(self):
        for cog in self.cogslist:
            await self.load_extension("cogs."+cog)

    async def on_ready(self):
        self.add_view(channel_system.VoiceButtons(client))
        self.add_view(ticket_system.TicketMenuView(client))
        self.add_view(ticket_system.TicketButtons(client))
        self.add_view(ticket_system.DeleteTicketButtons(client))

        os.system('cls' if os.name == 'nt' else 'clear')
        prfx = (Back.BLACK + Fore.CYAN + time.strftime("%H:%M:%S", time.gmtime()) + Back.RESET + Fore.WHITE + Style.NORMAL)
        print(prfx + " Logged in as " + Fore.BLUE + self.user.name)
        print(prfx + " Bot ID " + Fore.BLUE + str(self.user.id))
        print(prfx + " Discord Version " + Fore.BLUE+ discord.__version__)
        print(prfx + " Python Version " + Fore.BLUE + str(platform.python_version()))
        print (prfx + " Cogs Loaded " + Fore.BLUE + str(len(self.cogslist)))
        await self.tree.sync()
        synced = await self.tree.sync(guild=discord.Object(id=config["guild_id"]))
        print(prfx + " Slash CMDs Synced " + Fore.BLUE + str(len(synced)) + " Commands")
        print("")
        await client.change_presence(activity = discord.CustomActivity(name=config["bot_status"]))

if __name__ == "__main__":
    client = Client()
    client.remove_command('help')
    client.run(os.getenv('TOKEN'))