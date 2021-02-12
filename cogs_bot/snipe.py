#
#                               sThicc-bot Snipe.py | 2020 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
from discord.ext import commands
from discord import Embed as em
from datetime import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class snipe(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.snipe_cache = {}
        self.editsnipe_cache = {}

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        self.snipe_cache[message.channel.id] = message
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        self.editsnipe_cache[after.message.channel.id]: (before, after)
    
    
    @commands.command()
    @commands.has_role(744012353808498808)
    async def snipe(self, ctx):
        msg = self.snipe_cache[ctx.channel.id]
        e = em(
            title='IsThicc | Snipe',
            colour=discord.Colour.blue,
            description=f'{msg.author.mention} ({msg.author}):\n{msg.content}',
            timestamp=msg.created_at
        ).set_footer(
            text='Sniped message created at'
        )

        await ctx.send(embed=e)
        del self.snipe_cache[ctx.channel.id]
        
    @commands.command()
    @commands.has_role(744012353808498808)
    async def editsnipe(self, ctx):
        # TODO: Make this fetch a message?
        b = self.editsnipe_cache[ctx.channel.id][0]
        a = self.editsnipe_cache[ctx.channel.id][1]
        e = em(
            title='IsThicc | Edit Snipe',
            colour=discord.Colour.blue,
            description=f'{b.author.mention} ({b.author}):\n**Before:** {b.content}\n**After:** {a.content}',
            timestamp=datetime.utcnow()
            # TODO: Make the timestamp work?
            # timestamp=msg.created_at
        ).set_footer(
            text='Edit snipe message created at'
        )
        
        await ctx.send(embed=e)
        del self.editsnipe_cache[ctx.channel.id]
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#


def setup(bot):
    bot.add_cog(snipe(bot))
