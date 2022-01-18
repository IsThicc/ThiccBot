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
class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0  # TODO: Move index to a db select because this won't be persistent
        self.cache = []
        self.latest = None

        self.up_emoji   = '⬆️'
        self.down_emoji = '⬇️'

        self.suggestion_channel = config.suggestion_channel
        self.suggestion_submit_channel = config.suggestion_submit_channel

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id != self.suggestion_submit_channel or message.author.bot:
            return
        
        # content = re.sub(r'~~|\|\||__|\*\*|`+', "", message.content)
            
        self.index += 1
        
        embed = em(
            title=f"Suggestion #{self.index}",
            colour=discord.Colour.blue(),
            timestamp=datetime.datetime.utcnow(),
            description=message.content
        ).set_author(
            name=message.author,
            icon_url=message.author.avatar_url
        ).set_footer(
            text="Status: Pending"
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

        self.cache.append(msg.id)
        self.latest = msg

        #   saccept  [id]    (reason)
        #   sdeny    [id]    (reason)
        #   react with      ✅      to accept
        #   react with      ❎      to deny

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_role(config.admin_role)  # staff role
    async def saccept(self, ctx, *args):
        await self.confirm(ctx, list(args), True)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_role(config.admin_role)
    async def sdeny(self, ctx, *args):
        await self.confirm(ctx, list(args), False)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def confirm(self, ctx, args: list, accept: bool):

        # could be message id or suggestion index id
        uid = args.pop(0)
        reason = " ".join(arg for arg in args) if args else "No reason specified."

        async def do_thing(owner, target):
            embed = target.embeds[0]
            
            # ?saccept [id] (reason)
            if accept:
                if "Accepted" in embed.footer.text:
                    return await owner.send("That suggestion has already been accepted")

                embed.color = discord.Colour.green()
                embed.set_footer(text="Status: Accepted")

                await owner.send("Suggestion accepted")

            # ?sdeny [id] (reason)
            else:
                if "Denied" in embed.footer.text:
                    return await owner.send("That suggestion has already been denied")

                embed.color = discord.Colour.red()
                embed.set_footer(text="Status: Denied")

                await owner.send("Suggestion denied")

            if reason != "" or not reason.isspace():
                embed.description = embed.description + "\n\nReason: " + reason

            await target.edit(embed=embed)

        if len(uid) > 10:
            try:
                msg = self.bot.get_channel(self.suggestion_channel)
                msg = await msg.fetch_message(uid)
                await do_thing(ctx, msg)

            except Exception:
                return await ctx.send(f"No message with that ID found {e}")

        else:
            if self.latest.id == uid:
                return await do_thing(ctx, self.latest)

            for id in self.cache:
                if id == uid:
                    msg = self.bot.get_guild(739510335949635736)
                    msg = msg.get_channel(config.suggestion_channel)
                    msg = await msg.fetch_message(id)
                    return await do_thing(ctx, msg)

            await ctx.send("No suggestion with that ID found in the cache, try using a message ID instead")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener(name="on_raw_reaction_add")
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != self.suggestion_channel:
            return

        isthicc = self.bot.get_guild(739510335949635736)
        member  = isthicc.get_member(payload.user_id)

        if config.admin_role not in {role.id for role in member.roles}:
            return

        message = isthicc.get_channel(payload.channel_id)
        message = await message.fetch_message(payload.message_id)
        embed = message.embeds[0]
        emoji = str(payload.emoji)

        if emoji == self.up_emoji:  # "✅":
            embed.color = discord.Colour.green()
            embed.set_footer(text = "Status: Accepted")
            await message.edit(embed=embed)

        elif emoji == self.down_emoji:  # "❎":
            embed.color = discord.Colour.red()
            embed.set_footer(text = "Status: Denied")
            await message.edit(embed=embed)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Suggestions(bot))
