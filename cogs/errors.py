#
#                         ThiccBot Errors.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
from . import tickets
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Errors(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, tickets.InsufficientTicketPermissions):
            await ctx.message.delete()
            return await ctx.channel.send(embed=discord.Embed(
                title="You do not have permissions to execute this command in this ticket!",
                colour=discord.Colour.red()
            ), delete_after=10)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Errors(bot))
