import discord
from discord.ext import commands

class ReactionRoles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.isthicc = bot.get_guild(739510335949635736)
        
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.message_id == 804177369584631810: # change
            if str(payload.emoji) == "🔔":
                role = self.isthicc.get_role(804161887704973323)
                await payload.member.add_roles(role)
            elif str(payload.emoji) == "📊":
                role = self.isthicc.get_role(804161985679720458)
                await payload.member.add_roles(role)
            elif str(payload.emoji) == "💻":
                role = self.isthicc.get_role(804161946004881448)
                await payload.member.add_roles(role)
                
    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id == 804177369584631810: # change
            if str(payload.emoji) == "🔔":
                role = self.isthicc.get_role(804161887704973323)
                await payload.member.remove_roles(role)
            elif str(payload.emoji) == "📊":
                role = self.isthicc.get_role(804161985679720458)
                await payload.member.remove_roles(role)
            elif str(payload.emoji) == "💻":
                role = self.isthicc.get_role(804161946004881448)
                await payload.member.remove_roles(role)
                
                
                
def setup(bot):
    bot.add_cog(ReactionRoles(bot))
