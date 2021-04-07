#
#                          IsThicc-bot RR.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot   = bot
        self.guild = None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_ready(self):
        self.guild = self.bot.get_guild(739510335949635736)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 804177369584631810:

            member = self.guild.get_member(payload.user_id)
            if str(payload.emoji)   == "🔔":
                role = self.guild.get_role(804161887704973323)
                await member.add_roles(role)

            elif str(payload.emoji) == "📊":
                role = self.guild.get_role(804161985679720458)
                await member.add_roles(role)

            elif str(payload.emoji) == "💻":
                role = self.guild.get_role(804161946004881448)
                await member.add_roles(role)

            elif str(payload.emoji) == "⌛":
                role = self.guild.get_role(829165778321276949)
                await member.add_roles(role)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 804177369584631810:

            member = self.guild.get_member(payload.user_id)
            if str(payload.emoji)   == "🔔":
                role = self.guild.get_role(804161887704973323)
                await member.remove_roles(role)

            elif str(payload.emoji) == "📊":
                role = self.guild.get_role(804161985679720458)
                await member.remove_roles(role)

            elif str(payload.emoji) == "💻":
                role = self.guild.get_role(804161946004881448)
                await member.remove_roles(role)

            elif str(payload.emoji) == "⌛":
                role = self.guild.get_role(829165778321276949)
                await member.remove_roles(role)
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(ReactionRoles(bot))
