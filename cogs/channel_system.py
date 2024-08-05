import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import json
import os
import random

from main import config

guild_id = config["guild_id"]
join_channel = config["join_channel"]
with open("json/list_emoji.json", 'r', encoding='utf-8') as file:
    emoji = json.load(file)


class VoiceButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(emoji=emoji["lock"], custom_id="temp_lock_channel", row=0)
    async def lock_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    channel = self.client.get_channel(channel_id)

                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.connect=False
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)

                    #await channel.set_permissions(interaction.guild.default_role,connect=False)
                    await interaction.response.defer()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=emoji["unlock"], custom_id="temp_unlock_channel", row=1)
    async def unlock_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    channel = self.client.get_channel(channel_id)

                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.connect=True
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)
                    #await channel.set_permissions(interaction.guild.default_role,connect=True)
                    await interaction.response.defer()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=emoji["eye_off"], custom_id="temp_hide_channel", row=0)
    async def hide_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    channel = self.client.get_channel(channel_id)

                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.read_messages=False
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)
                    #await channel.set_permissions(interaction.guild.default_role,read_messages=False)
                    await interaction.response.defer()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=emoji["eye"], custom_id="temp_unhide_channel", row=1)
    async def unhide_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    channel = self.client.get_channel(channel_id)
                    role = channel.guild.default_role
                    overwrites = channel.overwrites
                    role_overwrites = overwrites.get(role, discord.PermissionOverwrite())
                    role_overwrites.read_messages=True
                    overwrites[role] = role_overwrites
                    await channel.edit(overwrites=overwrites)
                    #await channel.set_permissions(interaction.guild.default_role,read_messages=True)
                    await interaction.response.defer()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=emoji["edit"], custom_id="temp_edit_name", row=0)
    async def edit_name_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.send_modal(NameModal(self.client, channel_id))
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=emoji["users"], custom_id="temp_member_limit", row=0)
    async def member_limit_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    await interaction.response.send_modal(UserLimitModal(self.client, channel_id))
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=emoji["user_minus"], custom_id="temp_kick_user", row=1)
    async def kick_user_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    view = KickMenuView(self.client, channel_id)
                    await interaction.response.send_message(view=view, ephemeral=True)
                    view.message = await interaction.original_response()
                    #await interaction.response.send_message("Soon...",ephemeral=True)
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)

    @discord.ui.button(emoji=emoji["trash"], custom_id="temp_delete_channel", row=1)
    async def delete_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.voice:
            channel_id = interaction.user.voice.channel.id
            if str(channel_id) in self.client.temp_channels:
                if self.client.temp_channels[str(channel_id)]["channel_owner"] == interaction.user.id:
                    channel = self.client.get_channel(channel_id)
                    await channel.delete()
                    await interaction.response.defer()
                    return
                else:
                    await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)
                    return
        await interaction.response.send_message("❌ Du bist nicht in einem Temp-Kanal.", ephemeral=True)


class NameModal(ui.Modal):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(title="Interface")
        self.client = client
        self.channel_id = channel
    value = discord.ui.TextInput(label="Kanalname", placeholder="Wähle einen neuen Kanalnamen", min_length=2, max_length=10, style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        channel = self.client.get_channel(self.channel_id)
        if channel:
            await interaction.response.defer()
            await channel.edit(name=f"🔊｜{self.value.value}")

class UserLimitModal(ui.Modal):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(title="Interface")
        self.client = client
        self.channel_id = channel
    value = discord.ui.TextInput(label="Nutzerlimit", placeholder="0-99", min_length=1, max_length=2, style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        channel = self.client.get_channel(self.channel_id)
        if channel:
            try:
                value = int(self.value.value)
            except ValueError:
                value = 0
            await interaction.response.defer()
            await channel.edit(user_limit=value)


class KickMenu(discord.ui.UserSelect):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(placeholder="Wähle eine Option aus")
        self.client = client
        self.channel_id = channel

    async def callback(self, interaction: discord.Interaction):
        if str(self.channel_id) in self.client.temp_channels:
            if self.client.temp_channels[str(self.channel_id)]["channel_owner"] == interaction.user.id:
                if self.values[0].id == interaction.user.id:
                    await interaction.response.send_message("❌ Du kannst dich nicht selber kicken.", ephemeral=True)
                    return
                
                channel = self.client.get_channel(self.channel_id)
                member = channel.guild.get_member(self.values[0].id)
                if member in channel.members:
                    await member.move_to(None)
                    await interaction.response.defer()
                else:
                    await interaction.response.send_message(f"❌ Der Benutzer {member.mention} ist nicht in diesem Kanal.", ephemeral=True)
            else:
                await interaction.response.send_message("❌ Du bist nicht der Kanal Owner.", ephemeral=True)


class KickMenuView(discord.ui.View):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(timeout=15)
        self.add_item(KickMenu(client, channel))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, KickMenu):
                child.disabled = True
        if self.message:
            await self.message.edit(view=self)



class voice_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.temp_channels = {}

    @commands.Cog.listener("on_ready")
    async def on_ready(self):
        category = self.client.get_channel(config["temp_chanels_category"])
        if category is not None and isinstance(category, discord.CategoryChannel):
            for channel in category.voice_channels:
                if channel.id != join_channel:
                    await channel.delete()

    @commands.Cog.listener("on_voice_state_update")
    async def on_voice_state_update(self, member, before: discord.VoiceState, after: discord.VoiceState):
        if after.channel is not None and after.channel != before.channel:
            if after.channel.id == join_channel:
                category = self.client.get_channel(config["temp_chanels_category"])
                temp_channel = await category.create_voice_channel(name="🔊｜Temp Kanal")
                await member.move_to(temp_channel)
                await temp_channel.set_permissions(after.channel.guild.default_role,send_messages=True,attach_files=True,embed_links=True,add_reactions=True)
                self.client.temp_channels[str(temp_channel.id)] = {"channel_owner": member.id}

        if before.channel is not None and after.channel != before.channel:
            try:
                channel_id = before.channel.id
                if str(channel_id) in self.client.temp_channels:
                    if self.client.temp_channels[str(channel_id)]["channel_owner"] == member.id:
                        if len(before.channel.members) == 0:
                            await before.channel.delete()
                            del self.client.temp_channels[str(channel_id)]
                        else:
                            random_member = random.choice(before.channel.members)
                            self.client.temp_channels[str(channel_id)]["channel_owner"] = random_member.id


            except:
                return
            
async def setup(client:commands.Bot) -> None:
    await client.add_cog(voice_system(client))


