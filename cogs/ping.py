#
#                             IsThicc-bot Ping.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
from discord.ext import commands
from discord     import Embed, Color
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Ping(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    async def ping(self, ctx):

        ping = float(self.bot.latency * 1000)
        em   = Embed(title="IsThicc", color=Color.gold())

        if ping <=20:
            em.description = (f":green_circle: Latency: {ping:.0f}")

        elif ping <=50:
            em.description = (f":orange_circle: Latency: {ping:.0f}")

        else:
            em.description = {f":red_circle: Latency: {ping:.0f}"}
        
        return await ctx.send(embed=em)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Ping(bot))
