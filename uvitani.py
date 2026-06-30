import discord
from discord.ext import commands

class Uvitani(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # !!! SEM VLOŽ ID TVÉHO UVÍTACÍHO KANÁLU !!!
        self.UVITACI_KANAL_ID = 1521489648763932793 

    @commands.Cog.listener()
    async def on_member_join(self, member):
        # 1. POSLÁNÍ SOUKROMÉ ZPRÁVY (DM) NOVÁČKOVI
        try:
            await member.send(
                f"✨ **Ahoj {member.name}, vítej!** ✨\n\n"
                f"Jsem **Arwen** a provedu tě začátkem tvé cesty. "
                f"Než se ti odemkne zbytek serveru, musím zjistit, kam vlastně patříš.\n\n"
                f"Presuň se prosím na serveru do roomky role! "
                f"Podle tvých odpovědí ti přidělím tvou roli a otevřu ti celý náš svět. Hodně štěstí! "
            )
        except discord.Forbidden:
            # Pokud má uživatel zavřená DM, bot zprávu nepošle, ale nespadne
            print(f"Nepodařilo se poslat DM uživateli {member.name} (má vypnuté soukromé zprávy).")

        # 2. POSLÁNÍ VEŘEJNÉ ZPRÁVY DO KANÁLU #uvitani
        kanal = self.bot.get_channel(self.UVITACI_KANAL_ID)
        if kanal:
            await kanal.send(
                f"👋 **Vítám tě, {member.mention}!**\n"
                f"Arwen tě zdraví! Tvým prvním úkolem je dokončit rozřazovací kvíz. "
                f"Jakmile získáš svou roli, tento kanál ti zmizí a uvidíš zbytek serveru! 🌟"
            )

# Propojení s hlavním botem
async def setup(bot):
    await bot.add_cog(Uvitani(bot))