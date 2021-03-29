#
#                          IsThicc-bot Members.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio
from discord.ext import commands
from discord     import Embed as em
from datetime    import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Members(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_member_join(self, member):
        guild = self.bot.get_guild(739510335949635736)
        if member.guild.id != guild.id: return
        
        await member.add_roles(guild.get_role(744001626922287114))

        await asyncio.sleep(2)
        channel = self.bot.get_channel(796955089628954666)

        await channel.send(f'{member.mention}', delete_after=1)
        await channel.send(embed=em(
            title="Welcome to IsThicc Software!",
            description=f"""
Welcome to IsThicc Software {member.mention}!

Please check out <#739927724700860506> before you continue! And make sure to ask for support in <#744252916684161094> if you need any help!
            """,
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_thumbnail(url=member.avatar_url).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="Welcome to IsThicc Software!"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_member_remove(self, member):

        guild = self.bot.get_guild(739510335949635736)
        
        if member.guild.id != guild.id: return

        await self.bot.get_channel(796955089628954666).send(embed=em(
            title=f"{member} has left IsThicc Software!",
            description=f"""
{member} has left IsThicc Software! <a:sad:796961152579534868>
            """,
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"{member} has left IsThicc Software!"
        ))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Members(bot))
