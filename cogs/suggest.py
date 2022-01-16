#
#                          ThiccBot Suggest.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
from aiohttp.helpers import TimeoutHandle
import discord, asyncio, re, datetime
from discord import Embed as em
from discord import team
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.index = 0
        self.cache = []
        self.latest = None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id != 801929449124790353 or message.author.bot: return
        
        #content = re.sub(r'~~|\|\||__|\*\*|`+', "", message.content)
            
        self.index += 1
        
        embed = em( 
            colour      =   discord.Colour.aqua(),
            description =   message.content,
            title       =   f"Suggestion #{self.index}",
            timestamp   =   datetime.datetime.utcnow()
        ).set_author(
            name        =   message.author,
            icon_url    =   message.author.avatar_url
        ).set_footer(
            text        =   "Status: Pending"
        )

        if message.attachments:
            try:
               embed.set_image(url=attachment[0].url)
               if len(message.attachments) != 1:
                   embed.add_field("Attachments", "\n".join(a.url for a in message.attachments))
            except Exception as e:
                await message.channel.send(e)
 
        msg = await self.bot.get_channel(801929480875802624).send(embed=embed)

        await msg.add_reaction('⬆️')
        await msg.add_reaction('⬇️')

        await message.reply(f'{msg.jump_url}', delete_after=5, mention_author=False)
        await message.delete()

        self.cache.append(msg.id)
        self.latest = msg

    #   saccept  [id]    (reason)
    #   sdeny    [id]    (reason)
    #   react with      ✅      to accept
    #   react with      ❎      to deny

    @commands.command()
    @commands.has_role(858814638502576148) # staff role
    async def saccept(self, ctx, *args):
        self.confirm(ctx, args, True)

    @commands.command()
    @commands.has_role(858814638502576148)
    async def sdeny(self, ctx, *args):
        self.confirm(ctx, args, False)

    async def confirm(self, ctx, args, accept):

        # could be message id or suggestion index id
        uid = args.pop(0);
        reason = ""
        for arg in args:
            reason += " " + arg

        # # # # # # # # # # # #

        async def do_thing(owner, target):
            embed = target.embeds[0];
            
            # ?saccept [id] (reason)
            if accept:
                if "Accepted" in embed.footer:
                    return await owner.send("That suggestion has already been accepted")

                embed.color = discord.Colour.green()
                embed.set_footer(text = "Status: Accepted")

                await owner.send("Suggestion accepted")

            # ?sdeny [id] (reason)
            else:
                if "Denied" in embed.footer:
                    return await owner.send("That suggestion has already been denied")

                embed.color = discord.Colour.red()
                embed.set_footer(text = "Status: Denied")

                await owner.send("Suggestion denied")

            if reason != "":
                embed.description = embed.description + "\n\nReason: " + reason

            await target.edit(embeds = [embed])

        if len(uid) > 10:
            try:
                msg = await self.bot.get_channel(801929480875802624).fetch_message(uid)
                do_thing(ctx, msg)

            except:
                await ctx.send("No message with that ID found")

        else:
            if self.latest.id == uid:
                return do_thing(ctx, self.latest)

            for id in self.cache:
                if id == uid:
                    msg = await self.guild.get_channel(801929480875802624).fetch_message(id)
                    return do_thing(ctx, msg)

            await ctx.send("No suggestion with that ID found in the cache, try using a message ID instead")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        if payload.channel_id != 801929480875802624:
            return

        member = self.guild.get_member(payload.user_id)

        x = False
        for role in member.roles:
            if role.id == 744012353808498808:
                x = True
                break
        if not x:
            return

        message = self.guild.get_channel(payload.channel_id).fetch_message(payload.message_id)
        embed = message.embeds[0]
        emoji = str(payload.emoji)

        if emoji == "✅":
            embed.color = discord.Colour.green()
            embed.set_footer(text = "Status: Accepted")
            await message.edit(embeds = [embed])

        elif emoji == "❎":
            embed.color = discord.Colour.red()
            embed.set_footer(text = "Status: Denied")
            await message.edit(embeds = [embed])
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Suggestions(bot))
