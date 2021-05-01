#
#                         IsThicc-bot Listener.py | 2020-2021 (c) IsThicc
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

channels = [
    '838158218567614495' # test channel
]

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session  =  ClientSession()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id not in channels: return
        if not message.author.bot: return await message.delete()
        l = len(message.clean_content)
        if l < 30: 
            await message.author.send(content=f"Your message is {30-l} letters too short:\n```{message.content}```")
            await message.delete()
        elif l > 60:
            await message.author.send(content=f"Your message is {l-60} letters too long:\n```{message.content}```")
            await message.delete()

    async def outline_rquest(self):
        request = await self.session.post(f"uri")
        code = request.status

        if code == 403:
            pass
        elif code == 500:
            pass
        else:
            pass
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Listener(bot))
