#
#                            IsThicc-bot Github.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
from discord.ext import commands
from aiohttp     import ClientSession
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class GitHub(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session = ClientSession()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        if after.name != "project":
            return
        
        await self.session.post("http://10.42.0.4:5000/github/teams", headers={"Authorization": "", "Role": after.id})  # Request to github teams.
       
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(GitHub(bot))
