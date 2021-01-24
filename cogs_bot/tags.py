from datetime import datetime

import discord
from discord.ext import commands
from discord_slash import SlashContext, utils
from discord_slash import cog_ext as cmd

class Tags(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.slash = self.bot.slash
    
    async def perm_error(self, ctx):
        await ctx.send(embeds=[discord.Embed(description='Invalid Permissions! Only IsThicc staff can run this command!', colour=discord.Colour.red())])

    tagopts = [
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

    delopts = [
        {
            "name": "tag",
            "type": 3,
            "description": "Tag name",
            "required": True
        }
    ]
    
    async def template(self, ctx, reply_id: int = None):
        r = await self.bot.db.execute('SELECT tag, content, owner, date FROM tag WHERE command_id = ?', (ctx.command_id,))
        content = discord.Embed(title=r[0][0], description=r[0][1], colour=discord.Colour.teal(), timestamp=datetime.strptime(r[0][3], "%Y-%m-%d"))
        content.set_footer(text=f'Tag created by {r[0][2]}, Created At')
        if reply_id:
            try:
                msg = await ctx.channel.fetch_message(reply_id)
                return await msg.reply(content)
            except:
                await ctx.send(content='Message to reply to not found, sending normally.', hidden=True)
            
            await ctx.send(content=content)

    ids = [739510335949635736]

    @commands.Cog.listener()
    async def on_ready(self):
        tags = await self.bot.db.execute('SELECT * FROM tags')
        for tag in tags:
            owner = str(self.bot.get_user(int(tag[0][2]))) if owner else "Unknown"
            self.slash.add_slash_command(self.template, tag[0][1], guild_ids=self.ids, options=self.tagopts, description=f'IsThicc Support Tag By {owner}')

    @cmd.cog_subcommand(base='tag', name='create', guild_ids=ids, options=createopts)
    async def tag_create(self, ctx: SlashContext, name: str, content: str):
        staff = await self.bot.fetch_guild(739510335949635736)
        staff = staff.get_role(744012353808498808)

        if staff not in ctx.author.roles:
            return await self.perm_error(ctx)
        
        if name in self.bot.slash.commands.keys():
            return await ctx.send(content='Tag already exists with that name!', complete_hidden = True)

        self.slash.add_slash_command(self.template, name, guild_ids=self.ids, options=self.tagopts, description=f'IsThicc Support Tag By {owner}')
        await self.bot.db.add_tag(name, content, ctx.author.id, ctx.command_id)

        embed = discord.Embed(description=f'Created tag {name}!', colour=discord.Colour.green())

        await ctx.send(embeds=[embed])

    @cmd.cog_subcommand(base='tag', name='delete', guild_ids=ids, options=delopts)
    async def tag_delete(self, ctx: SlashContext, tag: str):
        staff = await self.bot.fetch_guild(739510335949635736)
        staff = staff.get_role(744012353808498808)

        if staff not in ctx.author.roles:
            return await self.perm_error(ctx)

        if tag not in self.bot.slash.commands.keys():
            return await ctx.send(content=f'Tag with the name {tag} does not exist!', complete_hidden = True)
        
        cmdid = self.bot.db.remove_tag(tag)

        utils.manage_commands.remove_slash_command(self.bot.user.id, self.bot.http.token, ctx.guild.id, cmdid)


def setup(bot):
    bot.add_cog(Tags(bot))
