#
#                          IsThicc-bot RR.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot   = bot
        self.guild = bot.get_guild(739510335949635736)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener() # Make the bot listen for a function
    async def on_raw_reaction_add(self, payload): # This is the function the bot is listening for
        if payload.message_id == 804177369584631810: # change
            if str(payload.emoji) == "🔔":
                role = self.guild.get_role(804161887704973323) # Fetch a discord.Role from our self.guild
                await payload.member.add_roles(role) # Give the payloads member the role(The member who reacted)
            elif str(payload.emoji) == "📊":
                role = self.guild.get_role(804161985679720458)
                await payload.member.add_roles(role)
            elif str(payload.emoji) == "💻":
                role = self.guild.get_role(804161946004881448)
                await payload.member.add_roles(role)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 804177369584631810: # change
            if str(payload.emoji) == "🔔":
                role = self.guild.get_role(804161887704973323)
                await payload.member.remove_roles(role) # Remove the role from the payloads member
            elif str(payload.emoji) == "📊":
                role = self.guild.get_role(804161985679720458)
                await payload.member.remove_roles(role)
            elif str(payload.emoji) == "💻":
                role = self.guild.get_role(804161946004881448)
                await payload.member.remove_roles(role)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(ReactionRoles(bot))
