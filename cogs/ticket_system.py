import discord
from discord.ext import commands
from discord import app_commands
from discord import ui
import json
import time

from main import config

ticket_category = config["ticket_category"]
ticket_staff = config["ticket_staff"]

with open("json/list_emoji.json", 'r', encoding='utf-8') as file:
    emoji = json.load(file)
with open("json/list_images.json", 'r', encoding='utf-8') as file:
    images = json.load(file)
with open("json/tickets.json", 'r') as file:
    tickets = json.load(file)

emojis = {
    "allgemein": "📨",
    "bewerbung": "📄",
    "community_server_bewerbung": "➕",
    "entbannung": "🚫"
}
reasons = {
    "allgemein": "Allgemein",
    "bewerbung": "Bewerbung",
    "community_server_bewerbung": "Community Server Bewerbung",
    "entbannung": "Entbannungsantrag"
}
color = {
    "grey": 0xa7acb4,
    "green": 0x248046,
    "red": 0xda373c
}

def save_to_json(location, content):
    with open(location, 'w') as file:
        json.dump(content, file, indent=4)

class ticket_system(commands.Cog):
    def __init__(self, client: commands.Bot):
        self.client = client
        self.client.ticket_list = tickets


async def setup(client:commands.Bot) -> None:
    await client.add_cog(ticket_system(client))
##########################################################################
class TicketMenu(discord.ui.Select):
    def __init__(self, client:commands.Bot):
        options = [discord.SelectOption(label="Allgemeiner Support", description="Allgemeiner Support / Fragen", emoji=emoji["mail"], value="allgemein"),
                   discord.SelectOption(label="Team Bewerbung", description="Bewirb dich als Teammitglied", emoji=emoji["file_text"], value="bewerbung"),
                   discord.SelectOption(label="Community Server Bewerbung", description="Bewirb dich für den Community Server", emoji=emoji["user_check"], value="community_server_bewerbung"),
                   discord.SelectOption(label="Entbannungsantrag", description="Beantrage einen Entbannungsantrag", emoji=emoji["block"], value="entbannung")]
        super().__init__(placeholder="Wähle eine Option aus", options=options, custom_id="ticket_options")
        self.client = client

    async def callback(self, interaction: discord.Interaction):
        value = self.values[0]
        if value == "community_server_bewerbung":
            if self.client.storage["community_server_status"] == "False":
                await interaction.response.send_message(f"❌ Der Community Server ist zurzeit geschlossen.", ephemeral=True)
                self.view.clear_items()
                self.view.add_item(TicketMenu(self.client))
                await interaction.message.edit(view=self.view)
                return

        for ticket in self.client.ticket_list.values():
            if ticket["ticket_owner"] == str(interaction.user.id):
                await interaction.response.send_message(f"❌ Du hast schon ein Ticket.", ephemeral=True)
                self.view.clear_items()
                self.view.add_item(TicketMenu(self.client))
                await interaction.message.edit(view=self.view)
                return
        if self.values[0] == "bewerbung":
            modal = StaffAppModal(self.client, value)
            await interaction.response.send_modal(modal)
        if self.values[0] != "bewerbung":        
            category = self.client.get_channel(ticket_category)
            ticket_channel = await category.create_text_channel(name=f"{emojis[value]}｜{interaction.user.name}")

            embed = discord.Embed(description=f"## Ticket erfolgreich erstellt\n\nDu hast erfolgreich ein Ticket mit dem Grund `{reasons[value]}` erstellt.\nNavigiere zum Kanal <#{ticket_channel.id}> um deine Konversation mit dem Team zu Starten.", color=color["green"])
            embed.set_image(url=images["green_ticket_line"])
            await interaction.response.send_message(embed=embed, ephemeral=True)


            await ticket_channel.set_permissions(ticket_channel.guild.default_role,read_messages=False, send_messages=False)
            await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
            for role_id in ticket_staff:
                role = interaction.guild.get_role(role_id)
                if role:
                    await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)


            embed = discord.Embed(title=f"{emoji["mail"]} TICKET", description=f"> **Ticket Informationen**\n > - Nutzer: {interaction.user.mention}\n > - Grund: `{reasons[value]}`\n> - Erstellt: <t:{int(time.time())}:R> \n\n> **Informationen an Nutzer**\n > - Bitte beschreibe dein Anliegen so genau wie möglich, damit das Team so schnell wie möglich helfen kann.\n > - Bitte habe etwas Geduld, bis das Team sich bei dir meldet.", color=color["grey"])
            embed.set_image(url=images["grey_ticket_line"])
            await ticket_channel.send(embed=embed, view=TicketButtons(self.client))

            self.client.ticket_list[str(ticket_channel.id)] = {"ticket_owner": str(interaction.user.id),"created_at": int(time.time())}
            save_to_json("json/tickets.json", self.client.ticket_list)

        self.view.clear_items()
        self.view.add_item(TicketMenu(self.client))
        await interaction.message.edit(view=self.view)

class StaffAppModal(ui.Modal):
    def __init__(self, client:commands.Bot, value):
        super().__init__(title="Ticket System")
        self.client = client
        self.reason = value
    value = discord.ui.TextInput(label="Bewerbungsart", placeholder="z.B. Twitch Mod, Discord Mod, ...", min_length=5, max_length=50, style=discord.TextStyle.short)
    async def on_submit(self, interaction: discord.Interaction):
        category = self.client.get_channel(ticket_category)
        ticket_channel = await category.create_text_channel(name=f"{emojis[self.reason]}｜{interaction.user.name}")

        embed = discord.Embed(description=f"## Ticket erfolgreich erstellt\n\nDu hast erfolgreich ein Ticket mit dem Grund `{reasons[self.reason]}` erstellt.\nNavigiere zum Kanal <#{ticket_channel.id}> um deine Konversation mit dem Team zu Starten.", color=color["green"])
        embed.set_image(url=images["green_ticket_line"])
        await interaction.response.send_message(embed=embed, ephemeral=True)


        await ticket_channel.set_permissions(ticket_channel.guild.default_role,read_messages=False, send_messages=False)
        await ticket_channel.set_permissions(interaction.user, read_messages=True, send_messages=True)
        for role_id in ticket_staff:
            role = interaction.guild.get_role(role_id)
            if role:
                await ticket_channel.set_permissions(role, read_messages=True, send_messages=True)


        embed = discord.Embed(title=f"{emoji["mail"]} TICKET", description=f"> **Ticket Informationen**\n > - Nutzer: {interaction.user.mention}\n > - Grund: `{reasons[self.reason]}`\n> - Bewerbungsart: `{self.value.value}`\n> - Erstellt: <t:{int(time.time())}:R> \n\n> **Informationen an Nutzer**\n > - Bitte beschreibe dein Anliegen so genau wie möglich, damit das Team so schnell wie möglich helfen kann.\n > - Bitte habe etwas Geduld, bis das Team sich bei dir meldet.", color=color["grey"])
        embed.set_image(url=images["grey_ticket_line"])
        await ticket_channel.send(embed=embed, view=TicketButtons(self.client))

        self.client.ticket_list[str(ticket_channel.id)] = {"ticket_owner": str(interaction.user.id),"created_at": int(time.time())}
        save_to_json("json/tickets.json", self.client.ticket_list)
##########################################################################
class TicketMenuView(discord.ui.View):
    def __init__(self, client:commands.Bot):
        super().__init__(timeout=None)
        self.add_item(TicketMenu(client))


class TicketButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(emoji=emoji["user_plus"], custom_id="remove_user_ticket", row=0)
    async def add_user_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == int(self.client.ticket_list[str(interaction.channel.id)]["ticket_owner"]):

            embed = discord.Embed(description=f"## Nutzer hinzufügen\n\nWähle unten den Nutzer aus, den du zu diesem Ticket hinzufügen möchtest, damit er dir helfen kann.", color=color["grey"])
            embed.set_image(url=images["user_plus_grey"])
            view = AddUserView(self.client, interaction.channel.id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message("❌ Du bist nicht der Ticket-Eigentümer.", ephemeral=True)

    @discord.ui.button(emoji=emoji["user_minus"], custom_id="add_user_ticket", row=0)
    async def remove_user_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        if interaction.user.id == int(self.client.ticket_list[str(interaction.channel.id)]["ticket_owner"]):

            embed = discord.Embed(description=f"## Nutzer entfernen\n\nWähle unten den Nutzer aus, den du zu diesem Ticket entfernen möchtest, da du ihn z.B. nicht mehr brauchst.", color=color["grey"])
            embed.set_image(url=images["user_minus_grey"])
            view = RemoveUserView(self.client, interaction.channel.id)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
            await interaction.response.send_message("❌ Du bist nicht der Ticket-Eigentümer.", ephemeral=True)

    @discord.ui.button(emoji=emoji["trash_red"], custom_id="close_ticket", row=0)
    async def close_ticket_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        #if interaction.user.id == int(self.client.ticket_list[str(interaction.channel.id)]["ticket_owner"]) or any(role.id in ticket_staff for role in interaction.user.roles) == True:
        if any(role.id in ticket_staff for role in interaction.user.roles) == True:
            embed = discord.Embed(description=f"## Ticket schließen\n\nMöchtest du wirklich dieses Ticket schließen? Klicke unten auf den roten Knopf, wenn du das Ticket schließen willst.", color=color["red"])
            embed.set_image(url=images["red_trash_line"])
            view = CloseConfirmButtons(self.client)
            await interaction.response.send_message(embed=embed, view=view, ephemeral=True)
            view.message = await interaction.original_response()
        else:
                await interaction.response.send_message("❌ Du bist nicht Ticket Staff.", ephemeral=True)

##########################################################################
class CloseConfirmButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=15)
        self.client = client
        self.message = None


    @discord.ui.button(emoji=emoji["trash"], style=discord.ButtonStyle.red, row=0)
    async def lock_channel_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        #await channel.delete()
        await interaction.response.defer()
        ticket_informations = self.client.ticket_list[str(interaction.channel.id)]
        embed = discord.Embed(title=f"{emoji["trash_red"]} TICKET GESCHLOSSEN", description=f"> **Log Informationen**\n > - Ticket Ersteller: <@{ticket_informations["ticket_owner"]}>\n> - Geschlossen von: {interaction.user.mention}\n> - Erstellt: <t:{ticket_informations["created_at"]}:t>\n> - Geschlossen: <t:{int(time.time())}:R> \n\n> **Kanal endgültig löschen**\n > - Wenn du diesen Kanal endgültig löschen möchtest, klicke unten auf den Lösch-Button.", color=color["red"])
        embed.set_image(url=images["red_trash_line"])

        channel = interaction.channel
        if str(channel.id) in self.client.ticket_list:
            del self.client.ticket_list[str(channel.id)]
            save_to_json("json/tickets.json", self.client.ticket_list)
        else:
            return

        overwrites = channel.overwrites
        for target, overwrite in overwrites.items():
            if isinstance(target, discord.Member):
                await channel.set_permissions(target, overwrite=None)

        current_name = channel.name
        new_name = '🔒' + current_name[1:]
        await channel.edit(name=new_name)


        await channel.send(embed=embed, view=DeleteTicketButtons(self.client))

    async def on_timeout(self):
        try:
            for item in self.children:
                item.disabled = True
            await self.message.edit(view=self)
        except:
            return


class DeleteTicketButtons(discord.ui.View):
    def __init__(self, client: commands.Bot):
        super().__init__(timeout=None)
        self.client = client

    @discord.ui.button(emoji=emoji["trash"], style=discord.ButtonStyle.red, custom_id="delete_ticket_channel", row=0)
    async def add_user_callback(self, interaction: discord.Interaction, Button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.channel.delete()
##########################################################################
class AddUserMenu(discord.ui.UserSelect):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(placeholder="Wähle eine Option aus")
        self.client = client
        self.channel_id = channel

    async def callback(self, interaction: discord.Interaction):
        if self.values[0].id == interaction.user.id:
            await interaction.response.send_message("❌ Du kannst dich nicht selber hinzufügen.", ephemeral=True)
            return
        channel = self.client.get_channel(self.channel_id)
        member = channel.guild.get_member(self.values[0].id)
        if member.bot:
            await interaction.response.send_message("❌ Du kannst APPs nicht hinzufügen.", ephemeral=True)
            return
        
        await interaction.response.send_message("✅ Nutzer erfolgreich hinzugefügt.", ephemeral=True)
        overwrite = discord.PermissionOverwrite()
        overwrite.view_channel = True
        overwrite.send_messages = True
        await channel.set_permissions(member, overwrite=overwrite)



class AddUserView(discord.ui.View):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(timeout=15)
        self.add_item(AddUserMenu(client, channel))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, AddUserMenu):
                child.disabled = True
        if self.message:
            await self.message.edit(view=self)
##########################################################################
class RemoveUserMenu(discord.ui.UserSelect):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(placeholder="Wähle eine Option aus")
        self.client = client
        self.channel_id = channel

    async def callback(self, interaction: discord.Interaction):
        if self.values[0].id == interaction.user.id:
            await interaction.response.send_message("❌ Du kannst dich nicht selber entfernen.", ephemeral=True)
            return
        channel = self.client.get_channel(self.channel_id)
        member = channel.guild.get_member(self.values[0].id)
        if member.bot:
            await interaction.response.send_message("❌ Du kannst APPs nicht entfernen.", ephemeral=True)
            return
        await interaction.response.send_message("✅ Nutzer erfolgreich entfernt.", ephemeral=True)
        await channel.set_permissions(member, overwrite=None)



class RemoveUserView(discord.ui.View):
    def __init__(self, client:commands.Bot, channel):
        super().__init__(timeout=15)
        self.add_item(RemoveUserMenu(client, channel))

    async def on_timeout(self):
        for child in self.children:
            if isinstance(child, RemoveUserMenu):
                child.disabled = True
        if self.message:
            await self.message.edit(view=self)