import discord
from discord.ext import commands

from discord_slash import cog_ext as cmd
from discord_slash import SlashContext

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash = self.bot.slash

    ids = [739510335949635736]
    

    tagops = [
        {
            "name": "reply",
            "type": 4,
            "description": "Message ID to reply to when sending tag content",
            "required": False
        }
    ]

    createopts = [
        {
            "name": "name",
            "type": 3,
            "description": "Tag name",
            "required": True
        },
        {
            "name": "content",
            "type": 3,
            "description": "Tag content",
            "required": True
        }
    ]

    @cmd.cog_subcommand(base='tag', name='create', options=createopts, guild_ids=ids)
    async def tag_create(self, ctx: SlashContext, name: str, content: str):
        
        await ctx.message.reply(embed=discord.Embed(description=f'Created the tag **{name}**!', colour=discord.Colour.green()))

def setup(bot):
    bot.add_cog(Tags(bot))