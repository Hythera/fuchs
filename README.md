<p align="center"><img src="https://github.com/Blackstonecoden/Fuchs-Bot/blob/main/images/bot_logo.png?raw=true" alt="Fuchs Bot Logo" width="200"></p>
<h1 align="center">Fuchs Bot - Python<br>
	<a href="https://github.com/Blackstonecoden/Fuchs-Bot"><img src="https://img.shields.io/github/stars/Blackstonecoden/Fuchs-Bot"></a>
	<a href="https://discord.gg/9QA8DVRKqw"><img src="https://img.shields.io/discord/1192851131760656435?color=5865f2&label=Discord&style=flat" alt="Discord"></a>
	<br><br>
</h1>

---

# Was ist der Fuchs Bot?

Der Fuchs Bot ist die Custom-Made APP für den Fuchs Höhle Discord Server. Die Features von der APP sind: WelcomeSystem, Counting System, Temp-Channel System, Ticket System und Level System.

--- 

# 1. Setup
## 1.1 Anforderungen
Wenn du einen eigene APP haben möchtest, erstelle zuerst eine auf [discord.com/developers](https://discord.com/developers/applications) und gib der APP alle intents. Klone den Code und packe ihn auf deinen Server. Sonstige Anforderungen:
- Server mit Python instaliert (um die APP zu hosten)
- MySQL / MariaDB Database

## 1.2 Config Setup
### 1.2.1 Umgebungsvariablen
Erstelle eine Date namens `.env` auf deinem Server und fülle sie mit deinen APP und Database Anmeldeinformationen.
```py
TOKEN = MTI...

database_host = 1.2.3.4:3306
database_user = nutzername
database_password = passwort
database_name = discord_app
```
### 1.2.2 Config Datei
Erstelle nun eine Datei namens `config.json` und fülle sie mit deinen Konfigurationen
```json
{
    "guild_id": 1234567890123456789,

    "join_role": 1234567890123456789,

    "welcome_channel": 1234567890123456789,

    "ticket_category": 1234567890123456789,
    "ticket_staff": [1234567890123456789,1234567890123456789],

    "join_channel": 1234567890123456789,
    "temp_chanels_category": 1234567890123456789,

    "counting_channel": 1234567890123456789,

    "daily_rewards": {
    "0": 100,
    "1": 200,
    "2": 300,
    "3": 400,
    "4": 500,
    "5": 600,
    "6": 700,
    "7": 1000
    },

    "bot_status": "🦊 Fuchs"
}
```
1.2.3 Json konfigurieren
Als nächstes startest du die APP, indem du die main.py ausführst und alle Abhängigkeiten aus `requirements.txt` instalierst. Dann sollte ein Ordner namens `json` erscheinen. Öffne die `list_images.json` und fülle sie mit folgendem Inhalt:

```json
{
    "interface_card": "https://raw.githubusercontent.com/Blackstonecoden/Fuchs/main/images/card.png",

    "grey_ticket_line": "https://raw.githubusercontent.com/Blackstonecoden/Fuchs/main/line_icons/ticket_grey.png",
    "red_ticket_line": "https://raw.githubusercontent.com/Blackstonecoden/Fuchs/main/line_icons/ticket_red.png",
    "green_ticket_line": "https://raw.githubusercontent.com/Blackstonecoden/Fuchs/main/line_icons/ticket_green.png",

    "user_plus_grey": "https://raw.githubusercontent.com/Blackstonecoden/Fuchs/main/line_icons/user_plus_grey.png",
    "user_minus_grey": "https://raw.githubusercontent.com/Blackstonecoden/Fuchs/main/line_icons/user_minus_grey.png",

    "red_trash_line": "https://raw.githubusercontent.com/Blackstonecoden/Fuchs/main/line_icons/trash_red.png"
}
```

Öffne nun die `list_emoji.json` und Füge deine Emojis (erstelle diese auf einem Discord Server oder auf deiner APP und kopiere deren ID und Namenin dem Format `<:name:id>`). Die Icons von der Haupt APP kommen von [feathericons.com](https://feathericons.com/).

```json
{
    "edit":"<:edit:12345678901234567890>",
    "eye":"<:eye:12345678901234567890>",
    "eye_off":"<:eye_off:12345678901234567890>",
    "lock":"<:lock:12345678901234567890>",
    "trash":"<:trash:12345678901234567890>",
    "unlock":"<:unlock:12345678901234567890>",
    "user_minus":"<:user_minus:12345678901234567890>",
    "user_plus": "<:user_plus:12345678901234567890>",
    "users":"<:users:12345678901234567890>",
    "user_check": "<:user_check:12345678901234567890",
    "file_text": "<:file_text:12345678901234567890>",
    "block": "<:block:12345678901234567890>",
    "mail":"<:mail:12345678901234567890>",
    "repeat":"<:repeat:12345678901234567890>",
    "zap": "<:zap:12345678901234567890>",
    "refresh": "<:refresh:12345678901234567890>",
    "dollar": "<:dollar:12345678901234567890>",

    "trash_red": "<:trash_red:12345678901234567890>"
}
```

## 1.3 APP starten
Nun sollte alles startklar sein und du kannst die main.py starten und die APP soltle fehlerfrei laufen. Falls du Hilfe benötigst, tritt gerne unserem [Discord Server](https://discord.gg/9QA8DVRKqw) bei.