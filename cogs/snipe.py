#
#                           Thicc-bot Snipe.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
from discord.ext import commands
from discord     import Embed as em
from datetime    import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class Snipe(commands.Cog):
    def __init__(self, bot):
        self.bot             = bot
        self.snipe_cache     = {}
        self.editsnipe_cache = {}

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_message_delete(self, message):     
        # if message.channel.id in self.editsnipe_cache:  # .keys():
        #     del self.snipe_cache[message.channel.id]
        self.snipe_cache[message.channel.id] = message

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # if after.channel.id in self.editsnipe_cache:  # .keys():
        #     del self.editsnipe_cache[after.channel.id]
        self.editsnipe_cache[after.channel.id] = (before, after)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_role(744012353808498808)
    async def snipe(self, ctx):

        if ctx.channel.id not in self.snipe_cache:  # .keys():
            return await ctx.send(embed=em(
                title='IsThicc | Error',
                description='Nothing to snipe!',
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ))

        msg = self.snipe_cache[ctx.channel.id]
        e   = em(
            title='IsThicc | Snipe',
            colour=discord.Colour.blue(),
            description=f'{msg.author.mention} ({msg.author}):\n{msg.content}',
            timestamp=msg.created_at
        ).set_footer(
            text='Sniped message sent at',
            icon_url=self.bot.user.avatar_url
        )

        await ctx.send(embed=e)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_role(744012353808498808)
    async def editsnipe(self, ctx):

        if ctx.channel.id not in self.editsnipe_cache:  # .keys():
            return await ctx.send(embed=em(
                title='IsThicc | Error',
                description='Nothing to editsnipe!',
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ))

        b = self.editsnipe_cache[ctx.channel.id][0]
        a = self.editsnipe_cache[ctx.channel.id][1]
        e = em(
            title='IsThicc | Edit Snipe',
            colour=discord.Colour.blue(),
            description=f'{b.author.mention} ({b.author}):\n**Before:** {b.content}\n**After:** {a.content}',
            timestamp=b.created_at
        ).set_footer(
            text='Edit snipe message sent at',
            icon_url=self.bot.user.avatar_url
        )
        
        await ctx.send(embed=e)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Snipe(bot))
