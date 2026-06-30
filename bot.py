import discord
from discord.ext import commands
import os
from flask import Flask
from threading import Thread

# Web server pro UptimeRobot
app = Flask('')
@app.route('/')
def home():
    return "Arwen je vzhůru a střeží server!"

def run():
    app.run(host='0.0.0.0', port=8080)

# Start web serveru v pozadí
t = Thread(target=run)
t.start()

# --- Zbytek tvého stávajícího kódu pro bota ---
intents = discord.Intents.default()
intents.message_content = True  
intents.members = True          

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"--- Sekce Funkcí Online ---")
    # ... (tady nech zbytek svého stávajícího kódu na načítání modulů) ...
    print(f"---------------------------")

bot.run(os.environ.get("DISCORD_TOKEN"))

intents = discord.Intents.default()
intents.message_content = True  
intents.members = True   # VELMI DŮLEŽITÉ: Bez tohoto zapnutého práva bot nepozná, že se někdo připojil!

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"--- Sekce Funkcí Online ---")
    print(f"Přihlášen jako: {bot.user}")
    
    # 1. Načtení modulu AUTOMOD
    try:
        await bot.load_extension("automod")
        print(" Modul AUTOMOD úspěšně spuštěn!")
    except Exception as e:
        print(f"❌ Chyba při načítání modulu AUTOMOD: {e}")
        
    # 2. Načtení modulu ANONYM
    try:
        await bot.load_extension("anonym")
        print(" Modul ANONYM úspěšně spuštěn!")
    except Exception as e:
        print(f"❌ Chyba při načítání modulu ANONYM: {e}")
        
    # 3. Načtení modulu UVÍTÁNÍ
    try:
        await bot.load_extension("uvitani")
        print(" Modul UVÍTÁNÍ úspěšně spuštěn!")
    except Exception as e:
        print(f"❌ Chyba při načítání modulu UVÍTÁNÍ: {e}")
        
    print(f"---------------------------")

bot.run(os.environ.get("DISCORD_TOKEN"))
