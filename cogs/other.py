#
#                             IsThicc-bot Other.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import random
from discord.ext import commands
from discord import Embed, Color, AllowedMentions
from aiohttp import ClientSession
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    async def ping(self, ctx):

        em   = Embed(title="IsThicc", color=Color.gold())
        ping = float(self.bot.latency * 1000)

        if ping <= 20:
            em.description = f":green_circle: Latency: {ping:.0f}"

        elif ping <= 50:
            em.description = f":orange_circle: Latency: {ping:.0f}"

        else:
            em.description = f":red_circle: Latency: {ping:.0f}"

        return await ctx.send(embed=em)

    # #  # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @commands.command()
    async def mock(self, ctx, *, message: str = None):
        if message is None:
            return await ctx.send("pLeAsE sUpPlY A mESsAgE tO mOcK")

        list = [random.choice([s.upper(), s.lower()]) for s in message]
        for char in range(len(list)):
            if list[char] == "!":
                list[char] = random.choice(["1", "!"])

        send = "".join(list)
        await ctx.send(send, allowed_mentions=AllowedMentions(roles=False, users=False, everyone=False))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @commands.command(aliases=["doge"])
    async def shiba(self, ctx):
        async with session.get("http://shibe.online/api/shibes") as req:
            json = await req.json()
            await ctx.send(embed=discord.Embed(colour=discord.Colour.teal()).set_image(url=json[0]))


#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

def setup(bot):
    bot.add_cog(Other(bot))
