#
#                         IsThicc-bot Status.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio
from discord.ext          import commands
from discord.ext.commands import BucketType
from discord              import Embed as em
from datetime             import datetime
from aiohttp              import ClientSession
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

urls = {
    'IsThicc'       : 'https://isthicc.dev/',
    'IsThicc API'   : 'https://api.isthicc.dev/',
    'IsThicc Paste' : 'https://paste.isthicc.dev/',
    'IsThicc GitHub': 'https://github.com/IsThicc',
    'Backend 1'     : 'http://10.42.0.1',
    'Backend 3'     : 'http://10.42.10.3',
    'Backend 4'     : 'http://10.42.10.4'
}

class Status(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session = ClientSession()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.cooldown(5, 1, BucketType.user)
    async def status(self, ctx):
        # Progress Bar Settings
        length = len(urls)
        bars = 25

        pending = await ctx.send(embed=em(
            title="Fetching URL's",
            description=f"Please wait while IsThicc writes a status report...",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Status"
                )
            )
        status_em = em(
            title="Status Report",
            description="IsThicc software status report.",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Status"
            ).set_thumbnail(url='https://rebin.ch/wp-content/uploads/2015/09/icon-2.png')

        i = 0
        for title, url in urls.items():
            # Progress Bar
            i += 1
            p = int(bars*i/length)
            p_bar = f"┤{(p*'█ ')}{((bars-p)*'─')}├ **({i}/{length})**"
            await pending.edit(embed=em(
                title="Fetching URL's",
                description=f"Please wait while IsThicc writes a status report...\n{p_bar}",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Status"
                    )
                )
            
            # Getting Status
            request = await self.session.get(url)
            code = request.status
            await asyncio.sleep(2)

            val = "unspecified"

            if code == 200  : val = "is working"
            elif code == 401: val = "bad request"
            elif code == 403: val = "forbidden"
            elif code == 404: val = "not found"
            elif code == 500: val = "server internal error"
              
            sym = "✓" if code == 200 else "✗"
            status_em.add_field(
                name=f"{sym} {title}",
                value=f"*[{title}]({url}) {val}. `{code}`*")

            request.close()
        
        await pending.edit(embed=status_em)
        # await pending.delete()

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Status(bot))
