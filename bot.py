import discord
from discord.ext import commands
import os

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

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Arwen je vzhůru!"

def run():
    app.run(host='0.0.0.0', port=8080)

t = Thread(target=run)
t.start()

bot.run(os.environ.get("DISCORD_TOKEN"))
