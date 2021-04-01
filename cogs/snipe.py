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
        # self.snipe_cache[message.channel.id] = message

        if message.channel.id not in self.snipe_cache:
            self.snipe_cache[message.channel.id] = \
                [None, None, None, None, None, None, None, None, None, None]

        # cache         = self.snipe_cache[message.channel.id]
        # temp_cache    = list(self.snipe_cache[message.channel.id])
        # temp_cache[9] = cache[8]
        # temp_cache[8] = cache[7]
        # temp_cache[7] = cache[6]
        # temp_cache[6] = cache[5]
        # temp_cache[5] = cache[4]
        # temp_cache[4] = cache[3]
        # temp_cache[3] = cache[2]
        # temp_cache[2] = cache[1]
        # temp_cache[1] = cache[0]
        # temp_cache[0] = message
        # self.snipe_cache[message.channel.id] = temp_cache

        cache = list(self.snipe_cache[message.channel.id])
        self.snipe_cache[message.channel.id] = list([message,  cache[0],
                                                     cache[1], cache[2],
                                                     cache[3], cache[4],
                                                     cache[5], cache[6],
                                                     cache[7], cache[8]])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        # if after.channel.id in self.editsnipe_cache:  # .keys():
        #     del self.editsnipe_cache[af                                 ter.channel.id]
        # self.editsnipe_cache[after.channel.id] = (before, after)

        if after.channel.id not in self.editsnipe_cache:
            self.editsnipe_cache[after.channel.id] = \
                [None, None, None, None, None, None, None, None, None, None]

        cache = list(self.editsnipe_cache[after.channel.id])
        self.editsnipe_cache[after.channel.id] = list([(before, after),
                                                       cache[0], cache[1],
                                                       cache[2], cache[3],
                                                       cache[4], cache[5],
                                                       cache[6], cache[7],
                                                       cache[8]])

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_role(744012353808498808)
    async def snipe(self, ctx, num="1"):

        if ctx.channel.id not in self.snipe_cache:  # .keys():
            return await ctx.send(embed=em(
                title='IsThicc | Error',
                description='Nothing to snipe!',
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ))

        if num == "all":
            snipe_all = em(
                title="IsThicc |Snipe",
                colour=discord.Colour.blue(),
                timestamp=datetime.utcnow()
            )
            for item_num, item in enumerate(self.snipe_cache[ctx.channel.id]):
                if item is None: continue
                snipe_all.add_field(
                    name=f"Edit Snipe {item_num + 1}",
                    value=f'{item.author.mention} ({item.author}):\n{item.content}'
                )
            snipe_all.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Software"
            )
            return await ctx.send(embed=snipe_all)

        try: num = int(num)
        except: return await ctx.send(embed=em(
            title="Error!",
            description="Make sure you're inputting a valid integer between 1 and 10! Ex: 3",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Software"
        ))

        if num <= 0 or num >= 11:
            return await ctx.send(embed=em(
                title="Error!",
                description="Not a valid integer between 1 and 10!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Software"
            ))

        if self.snipe_cache[ctx.channel.id][num] is None:
            return await ctx.send(embed=em(
                title='IsThicc | Error',
                description='Nothing to snipe!',
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ))

        msg = self.snipe_cache[ctx.channel.id][num]
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
    async def editsnipe(self, ctx, num="1"):

        if ctx.channel.id not in self.editsnipe_cache:  # .keys():
            return await ctx.send(embed=em(
                title='IsThicc | Error',
                description='Nothing to editsnipe!',
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ))

        if num == "all":
            editsnipe_all = em(
                title="IsThicc | Edit Snipe",
                colour=discord.Colour.blue(),
                timestamp=datetime.utcnow()
            )
            for item_num, item in enumerate(self.editsnipe_cache[ctx.channel.id]):
                if item is None: continue
                b = item[0]
                a = item[1]
                editsnipe_all.add_field(
                    name=f"Edit Snipe {item_num + 1}",
                    value=f'{b.author.mention} ({b.author}):\n**Before:** {b.content}\n**After:** {a.content}'
                )
            editsnipe_all.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Software"
            )
            return await ctx.send(embed=editsnipe_all)

        try: num = int(num)
        except: return await ctx.send(embed=em(
            title="Error!",
            description="Make sure you're inputting a valid integer between 1 and 10! Ex: 3",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Software"
        ))

        if num <= 0 or num >= 11:
            return await ctx.send(embed=em(
                title="Error!",
                description="Not a valid integer between 1 and 10!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Software"
            ))

        if self.editsnipe_cache[ctx.channel.id][num] is None:
            return await ctx.send(embed=em(
                title='IsThicc | Error',
                description='Nothing to editsnipe!',
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ))

        b = self.editsnipe_cache[ctx.channel.id][num][0]
        a = self.editsnipe_cache[ctx.channel.id][num][1]
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
