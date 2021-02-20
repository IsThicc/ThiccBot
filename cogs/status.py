#
#                              IsThicc-bot Status.py | 2020 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio
from discord.ext import commands
from discord.ext.commands import BucketType
from discord import Embed as em
from datetime import datetime
from aiohttp import ClientSession
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

urls = {
    'IsThicc' : 'https://isthicc.xyz/',
    'IsThicc / Privacy Policy' : 'https://isthicc.xyz/privacy-policy/',
    'IsThicc / Services' : 'https://isthicc.xyz/services/'
}

class status_cog(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session = ClientSession()

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def status(self, ctx):

        status_em = em(
            title="Global Status Report",
            description="IsThicc Software management status report.",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ).set_thumbnail(url='https://rebin.ch/wp-content/uploads/2015/09/icon-2.png')

        for title, url in urls.items():
            r = await self.session.get(url)
            code = r.status
            await asyncio.sleep(2)

            val = "unspecified"

            if code == 200: val = "is working"
            elif code == 401: val = "bad request"
            elif code == 403: val = "forbidden"
            elif code == 404: val = "not found"
            elif code == 500: val = "server internal error"

            sym = "✓" if code == 200 else "✗"
            status_em.add_field(
                name=f"{sym} {title} ({url})",
                value=f"*{title} {val}. `{code}`*")
            r.close()
        await ctx.send(embed=status_em)


#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(status_cog(bot))
