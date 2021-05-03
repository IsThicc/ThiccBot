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
from datetime             import datetime as d, timedelta 
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

channels = [
    838158218567614495 # test channel
]

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Listener(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session =  ClientSession()
        
        self.bot.verify_cache = {}

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    @commands.Cog.listener()
    async def on_message(self, message):
        
        if message.channel.id not in channels: 
            return
        
        elif message.author.bot: 
            return await message.delete()
        
        id = message.author.id
        c  = message.channel
        
        if id in self.bot.verify_cache:
            if self.bot.verify_cache[id]['tries'] >= 4:
                if not self.bot.verify_cache[id]['last_try'] >= (d.now() - timedelta(minutes=10)):
                    await message.delete()
                    return await c.send(embed=em(title="You are being ratelimited!", 
                                                 description="Sorry! You have attempted to verify too many times! Please wait 10 minutes!",
                                                 colour=discord.Colour.red()), delete_after=10)
                
        else:
            self.bot.verify_cache[id]             = {}    
            self.bot.verify_cache[id]['last_try'] = d.now()
            self.bot.verify_cache[id]['tries']    = 0
        
        l = len(message.clean_content)
        
        if l < 30: 
            await c.send(content=f"Your message is {30-l} letters too short:\n```{message.content}```")
            await message.delete()
        
        elif l > 60:
            await c.send(content=f"Your message is {l-60} letters too long:\n```{message.content}```")
            await message.delete()
            
        else:
            await message.delete()
            request = await self.session.post(f"http://127.0.0.1:2003/", headers={"Authorization": "fill in config token here", "AuthToken": message.clean_content})
            code    = request.status

            if code == 200:
                return await c.send(embed=em(title="Verified!", 
                                             colour=discord.Colour.green(),
                                             description="You have been verified on the IsThicc Dashboard!"), delete_after=10)

            if code == 403:
                return await c.send(embed=em(title="Unable to verify!", 
                                             description="Sorry! Your provided ID is not valid! Please make sure you copy the exact ID from [here](https://isthicc.dev/dash/discord).",
                                             colour=discord.Colour.red()), delete_after=10)

            else:
                return await c.send(embed=em(title="An internal error has occurred!", 
                                             description=f"Please let IsThicc management know that an internal error has occurred! Please provide the status code!\nStatus code: {code}",
                                             colour=discord.Colour.red()), delete_after=10)
            
            request.close()
        
        self.bot.verify_cache[id]['tries']    += 1
        self.bot.verify_cache[id]['last_try']  = d.now()
        
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Listener(bot))
