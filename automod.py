import discord
from discord.ext import commands
from datetime import datetime, timedelta
import collections

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        # !!! SEM VLOŽ ID KANÁLU PRO MODERÁTORY !!!
        self.MOD_KANAL_ID = 1514184295219204156  
        
        # Seznam zakázaných slov
        self.ZAKAZANA_SLOVA = [
            # Obecné vulgarismy
            "debil", "kretén", "kreten", "idiot", "kokot", "píča", "pica", "čurák", "curak",
            "mrcha", "děvka", "devka", "kurva", "zmrd", "hovno", "srač", "sráč", "srac", "prdel", 
            "zkurv", "zkurvysyn", "píčus", "picus", "vyjeb", "naser", "chcíp", "chcípni", "chcip", "kunda", "mrdal", 
            "mrdat", "šoustat", "soustat", "čubka", "cubka", "bitch", "fuck", "dick", "cunt", 
            "pussy", "retard", "kráva", "krava", "vůl", "vul",
            
            # Rasistické a xenofobní urážky
            "negr", "nigga", "nigger", "cigán", "cigan", "černej", "cernej", "čmoud", "cmoud",
            "dežo", "dezo", "gádžo", "gadzo", "ruksak", "asfalt", "rákosník", "rakosnik", 
            "žluťák", "zlutak", "terorista", "rušák", "rusak", "ukáčko", "ukacko", "bambuch",
            
            # Homofobní a transfobní urážky
            "buzna", "teplouš", "teplous", "buzerant", "teplej", "buzy", "faggot", "fag", 
            "lesbař", "lesbar", "trandák", "trandak", "transka", "hermafrodit"
        ]
        
        # Paměť bota
        self.user_warnings = {}      # {user_id: pocet_varovani}
        self.last_reset_date = datetime.utcnow().date() # Sledování dne pro půlnoční reset
        self.user_msg_times = collections.defaultdict(list)

    def zkontroluj_půlnoční_reset(self):
        """Pokud nastal nový den, vymaže všechna varování."""
        dnes = datetime.utcnow().date()
        if dnes != self.last_reset_date:
            self.user_warnings.clear()
            self.last_reset_date = dnes
            print("Půlnoc proběhla: Počty varování byly vyresetovány.")

    async def pridej_varovani(self, user, channel, duvod):
        # Nejdřív zkontrolujeme, jestli už není nový den
        self.zkontroluj_půlnoční_reset()

        user_id = user.id
        if user_id not in self.user_warnings:
            self.user_warnings[user_id] = 0

        # Přičteme varování
        self.user_warnings[user_id] += 1
        pocet_varovani = self.user_warnings[user_id]

        # Poslat varování uživateli DO SOUKROMÉ ZPRÁVY (DM)
        try:
            await user.send(
                f"⚠️ **Varování na serveru!**\n"
                f"Tvá zpráva v kanále {channel.mention} byla smazána.\n"
                f"Důvod: *{duvod}*\n"
                f"Aktuální počet varování pro dnešní den: **{pocet_varovani}/3**."
            )
        except discord.Forbidden:
            # Pokud má uživatel zavřená DM, bot mu zprávu poslat nemůže (abychom předešli chybě)
            pass

        # Při dosažení 3 varování pošleme echo moderátorům
        if pocet_varovani == 3:
            mod_kanal = self.bot.get_channel(self.MOD_KANAL_ID)
            if mod_kanal:
                await mod_kanal.send(
                    f" **Hlášení pro moderátory!** \n"
                    f"Uživatel {user.mention} (ID: `{user.id}`) dnes nasbíral **3 varování**!\n"
                    f"Poslední prohřešek: *{duvod}* v kanále {channel.mention}.\n"
                    f"Počítadlo se mu vyresetuje dnes o půlnoci. "
                )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user or message.guild is None:
            return

        now = datetime.utcnow()
        user_id = message.author.id

        # --- 1. ANTI-SPAM ---
        self.user_msg_times[user_id].append(now)
        self.user_msg_times[user_id] = [t for t in self.user_msg_times[user_id] if now - t < timedelta(seconds=5)]

        if len(self.user_msg_times[user_id]) > 4:
            try:
                await message.delete()
            except:
                pass
                
            if len(self.user_msg_times[user_id]) == 5:
                await self.pridej_varovani(message.author, message.channel, "Spamování chatu")
            return

        # --- 2. KONTROLA NADÁVEK ---
        if any(slovo in message.content.lower() for slovo in self.ZAKAZANA_SLOVA):
            try:
                await message.delete()
            except:
                pass
            await self.pridej_varovani(message.author, message.channel, "Nevhodný slovník (nadávky)")
            return

# Propojení s hlavním botem
async def setup(bot):
    await bot.add_cog(AutoMod(bot))