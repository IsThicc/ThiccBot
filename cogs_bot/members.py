#
#           IsThicc-bot Members.py | 2020 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
import asyncio
from discord.ext import commands
from discord.ext.commands import BucketType
from discord import Embed as em
from datetime import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.where_am_i = "IsThicc Software"

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.Cog.listener()
    async def on_member_join(self, member):

        await asyncio.sleep(2)
        channel = self.bot.get_channel(796955089628954666)

        welcome = em(
            title=f"Welcome to {self.where_am_i}!",
            description=f"""
Welcome to {self.where_am_i} {member.mention}!

Please check out <#739927724700860506> before you continue! And make sure to ask for support in <#744252916684161094> if you need any help!
            """,
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        )
        welcome.set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"Welcome to {self.where_am_i}!"
        )
        welcome.set_thumbnail(url=member.avatar_url)
        msg = await channel.send(f'{member.mention}')
        await channel.send(embed=welcome, delete_after=1)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.Cog.listener()
    async def on_member_remove(self, member):

        channel = self.bot.get_channel(796955089628954666)

        welcome = em(
            title=f"{member} has left {self.where_am_i}!",
            description=f"""
{member} has left {self.where_am_i}! <a:sad:796961152579534868>
            """,
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        )
        welcome.set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"{member} has left {self.where_am_i}!"
        )
        await channel.send(embed=welcome)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(members(bot))
