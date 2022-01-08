#
#                             ThiccBot Other.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import random, aiohttp
from discord import Embed, Colour, AllowedMentions
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Other(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    async def ping(self, ctx):

        em   = Embed(title="IsThicc", color=Colour.gold())
        ping = float(self.bot.latency * 1000)

        if ping <= 20:
            em.description = f":green_circle: Latency: {ping:.0f}"

        elif ping <= 50:
            em.description = f":orange_circle: Latency: {ping:.0f}"

        else:
            em.description = f":red_circle: Latency: {ping:.0f}"

        return await ctx.send(embed=em)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    def _mock_message(self, message: str) -> str:
        chars = [random.choice([s.upper(), s.lower()]) for s in message]
        for char in range(len(chars)):
            if chars[char] == "!":
                chars[char] = random.choice(["1", "!"])

        return "".join(chars)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    async def mock(self, ctx, *, message: str = None):
        if message is None:
            return await ctx.send(self._mock_message("Please supply a message to mock!"))

        send = self._mock_message(message)
        await ctx.send(send, allowed_mentions=AllowedMentions(roles=False, users=False, everyone=False))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # 

    @commands.command(aliases=["doge"])
    async def shiba(self, ctx):
        async with self.session.get("http://shibe.online/api/shibes") as req:
            json = await req.json()
            await ctx.send(embed=Embed(colour=Colour.teal()).set_image(url=json[0]))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

def setup(bot):
    bot.add_cog(Other(bot))
