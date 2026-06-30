import discord
from discord.ext import commands

class Anonym(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # !!! SEM VLOŽ ID SVÉHO ANONYMNÍHO KANÁLU !!!
        self.ANONYMNI_KANAL_ID = 1514187152689336360
    @commands.command(name="anonym")
    async def anonym_command(self, ctx, *, text: str):
        # Kontrola, zda píše do správného kanálu
        if ctx.channel.id != self.ANONYMNI_KANAL_ID:
            try:
                await ctx.message.delete()
            except:
                pass
            await ctx.author.send(" Příkaz `!anonym` můžeš používat pouze v určeném anonymním kanále.")
            return

        # Smazání původní zprávy od uživatele
        try:
            await ctx.message.delete()
        except:
            pass

        # Odeslání čistého textu přímo za Arwen
        await ctx.send(text)

    # Sledování odpovědí ve vláknech (anonymní diskuse)
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        # Kontrola, jestli se zpráva nachází ve vláknu (Thread)
        if isinstance(message.channel, discord.Thread):
            # Kontrola, jestli toto vlákno patří pod náš anonymní kanál
            if message.channel.parent_id == self.ANONYMNI_KANAL_ID:
                text = message.content
                
                # Smaže zprávu uživatele ve vláknu
                try:
                    await message.delete()
                except:
                    pass
                
                # Arwen ji pošle za sebe do stejného vlákna
                await message.channel.send(text)

# Propojení s hlavním botem
async def setup(bot):
    await bot.add_cog(Anonym(bot))