#
#                              IsThicc-bot Help.py | 2020 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
from discord.ext import commands
from discord.ext.commands import BucketType
from discord import Embed as em
from datetime import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def help(self, ctx):
        """
        "Help" command. Send a nice embed to show IsThicc help.
        :param ctx: Basic Discord.py context.
        :return: Returns Help embed.
        """

        # TODO: Check if person has staff role, then display a different embed

        return await ctx.send(embed=em(
            title="IsThicc Help!",
            description="""
The IsThicc bot is a work-in-progress bot to help our staff with server management!

The IsThicc Bot doesn't currently have any public commands! Please check back later. If you have questions with the bot or any of questions please don't hesitate to reach out to our staff in <#744252916684161094>!
            """,
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            text="IsThicc Software",
            icon_url=self.bot.user.avatar_url
        ))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(help(bot))
