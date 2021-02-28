#
#                          IsThicc-bot Application.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
from discord.ext import commands
from aiohttp import ClientSession
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class github_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession()


    @commands.cog.listener()
    async def on_guild_role_update(self, before, after):
        if after.name != "project":
            return
        
        self.session.post({"Authorization": "http://10.42.0.4:5000/github/teams", "Role": roleid := after.id}) # Request to github teams.
        

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(github_cog(bot))
