#
#                          ThiccBot Suggest.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, re, datetime, config
from discord import Embed as em, team
from discord.ext import commands
from aiohttp.helpers import TimeoutHandle
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

#   saccept  [id]    (reason)
#   sdeny    [id]    (reason)
#   react with      ✅      to accept
#   react with      ❎      to deny

class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

        self.up_emoji   = '⬆️'
        self.down_emoji = '⬇️'

        self.suggestion_channel = config.suggestion_channel
        self.suggestion_submit_channel = config.suggestion_submit_channel
        
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id != self.suggestion_submit_channel or message.author.bot:
            return
        
        #content = re.sub(r'~~|\|\||__|\*\*|`+', "", message.content)
            
        index = 1

        if self.bot.db.execute("SELECT COUNT(*) FROM suggestions;") != 0:
            index = self.bot.db.execute("SELECT MAX(index) FROM suggestions;") + 1

        embed = em( 
            title       =   f"Suggestion #{index}",
            description =   message.content,
            colour      =   discord.Colour.blue(),
            timestamp   =   datetime.datetime.utcnow()
        ).set_author(
            name        =   message.author,
            icon_url    =   message.author.avatar_url
        ).set_footer(
            text        =   "Status: Pending"
        )

        if message.attachments:
            try:
                embed.set_image(url=message.attachments[0].url)
                if len(message.attachments) != 1:
                    embed.add_field("Attachments", "\n".join(a.url for a in message.attachments))
            except Exception as e:
                await message.channel.send(e)
 
        msg = await self.bot.get_channel(self.suggestion_channel).send(embed=embed)

        await msg.add_reaction(self.up_emoji)
        await msg.add_reaction(self.down_emoji)

        await message.reply(f'{msg.jump_url}', delete_after=5, mention_author=False)
        await message.delete()

        sql = "INSERT INTO suggestions (owner, index, id, content, status, reason) VALUES (%s, %s, %s, %s, %s, %s);"
        sql = sql % (message.author.id, index, message.id, message.content, None, None)
        
        await self.bot.db.execute(sql)

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.channel_id != 801929480875802624:
            return;
        
        if await self.db.execute(f"SELECT COUNT(id) FROM suggestions WHERE id = {message.id};") > 0:
            await self.db.execute(f"DELETE FROM suggestions WHERE WHERE id = {message.id};")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != self.suggestion_channel:
            return

        if await self.db.execute(f"SELECT COUNT(id) FROM suggestions WHERE id = {payload.message_id};") == 0:
            return

        isthicc = self.bot.get_guild(739510335949635736)
        member  = isthicc.get_member(payload.user_id)

        if config.admin_role not in {role.id for role in member.roles}:
            return

        message = isthicc.get_channel(payload.channel_id)
        message = await message.fetch_message(payload.message_id)
        embed = message.embeds[0]
        emoji = str(payload.emoji)

        if emoji == self.up_emoji:
            embed.color = discord.Colour.green()
            embed.set_footer(text = "Status: Accepted")
            await message.edit(embeds = [embed])

            sql = f"UPDATE suggestions SET status = True WHERE id = {payload.message_id};"
            await self.bot.db.execute(sql)

        elif emoji == self.down_emoji:
            embed.color = discord.Colour.red()
            embed.set_footer(text = "Status: Denied")
            await message.edit(embeds = [embed])

            sql = f"UPDATE suggestions SET status = False WHERE id = {payload.message_id};"
            await self.bot.db.execute(sql)
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_role(858814638502576148) # staff role
    async def saccept(self, ctx, *args):
        await self.confirm(ctx, list(args), True)

    @commands.command()
    @commands.has_role(858814638502576148)
    async def sdeny(self, ctx, *args):
        await self.confirm(ctx, list(args), False)

    async def confirm(self, ctx, args, accept):

        async def do_thing(owner, target):
            reason = " ".join(arg for arg in args) if args else "No reason specified."
            embed = target.embeds[0];
            
            # ?saccept [id] (reason)
            if accept:
                if "Accepted" in embed.footer.text:
                    return await owner.send("That suggestion has already been accepted")

                embed.color = discord.Colour.green()
                embed.set_footer(text = "Status: Accepted")

                await owner.send("Suggestion accepted")

                sql = f"UPDATE suggestions SET status = True, reason = {reason} WHERE id = {target.id};"
                await self.db.execute(sql)

            # ?sdeny [id] (reason)
            else:
                if "Denied" in embed.footer.text:
                    return await owner.send("That suggestion has already been denied")

                embed.color = discord.Colour.red()
                embed.set_footer(text = "Status: Denied")

                await owner.send("Suggestion denied")

                sql = f"UPDATE suggestions SET status = False, reason = {reason} WHERE id = {target.id};"
                await self.db.execute(sql)

            if reason != "" or not reason.isspace():
                embed.description = embed.description + "\n\nReason: " + reason

            await target.edit(embed=embed)

        # # # # # # # # # # # # 

        # could be message id, suggestion index or nothing to get the latest sent suggestion in the channel
        uid = args.pop(0) if args[0].isdigit() else None;
        channel = self.bot.get_channel(self.suggestion_channel)

        # # # # # # # # # # # # 
        
        if uid == None:
            return await do_thing(ctx, await channel.fetch_message(channel.last_message_id))

        if await self.db.execute(f"SELECT COUNT(id) FROM suggestions WHERE index = {uid};") != 0:
            ids = await self.db.execute(f"SELECT id FROM suggestions")

            # TODO: Check this loop pls!!
            for item in ids:
                if item == uid:
                    return await do_thing(ctx, await channel.fetch_message(item))

        elif await self.db.execute(f"SELECT COUNT(id) FROM suggestions WHERE id = {uid};") != 0:
            await do_thing(ctx, await channel.fetch_message(uid))

        await ctx.send("No suggestion with that ID or index found in the db")

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Suggestions(bot))
