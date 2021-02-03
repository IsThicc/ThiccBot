#
#                          IsThicc-bot Tickets.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio
from discord.ext import commands
from discord import Embed as em
from datetime import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class mod(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.avatar  = bot.user.avatar_url

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, reason = "Banned from IsThicc Software", *):

        lets_make_sure = em(
            title=f"Are you sure you want to ban {member.display_name}?",
            colour=discord.Colour.dark_red(),
            timestamp=datetime.utcnow()
        )
        lets_make_sure.set_footer(
            icon_url=self.avatar,
            text="IsThicc Moderation"
        )
        msg = await ctx.send(embed=lets_make_sure)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        try:

            def yes_no(reaction, user):
                return user.id == ctx.author.id and reaction.channel.id == ctx.channel.id

            reaction, user = await self.bot.user.wait_for('reaction_add', check=yes_no, timeout=60)

        except asyncio.TimeoutError:

            timeout = em(
                title="Timed out!",
                description="You timed out! make sure to react within 60 seconds next time!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            timeout.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            await msg.clear_reactions()
            return await msg.edit(embed=timeout)

        await msg.clear_reactions()
        emoji = str(reaction.emoji)

        if emoji == '👍':

            bye_hoe = em(
                title="You have been banned from IsThicc Software!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            bye_hoe.add_field(
                name="Reason:",
                value=reason
            )
            bye_hoe.add_field(
                name="Banned by:",
                value=ctx.author
            )
            bye_hoe.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            try:

                await member.send(embed=bye_hoe)
                await member.ban(reason=reason)

            except Exception:
                ohno = em(
                    title="Uh oh!",
                    description=f"Sorry! I couldn't ban {member.mention}! Please make sure I have proper permissions!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                )
                ohno.set_footer(
                    icon_url=self.avatar,
                    text="IsThicc Moderation"
                )
                return await msg.edit(embed=ohno)

            ded = em(
                title="Banned!",
                description=f"I banned {member} for {reason}!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            )
            ded.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            return await msg.edit(embed=ded)

        else:
            no = em(
                title=f"I won't ban {member}!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            )
            no.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            return await msg.edit(embed=no)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, reason = "Kicked from IsThicc Software", *):

        lets_make_sure = em(
            title=f"Are you sure you want to kick {member.display_name}?",
            colour=discord.Colour.dark_red(),
            timestamp=datetime.utcnow()
        )
        lets_make_sure.set_footer(
            icon_url=self.avatar,
            text="IsThicc Moderation"
        )
        msg = await ctx.send(embed=lets_make_sure)
        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        try:

            def yes_no(reaction, user):
                return user.id == ctx.author.id and reaction.channel.id == ctx.channel.id

            reaction, user = await self.bot.user.wait_for('reaction_add', check=yes_no, timeout=60)

        except asyncio.TimeoutError:

            timeout = em(
                title="Timed out!",
                description="You timed out! make sure to react within 60 seconds next time!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            timeout.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            await msg.clear_reactions()
            return await msg.edit(embed=timeout)

        await msg.clear_reactions()
        emoji = str(reaction.emoji)

        if emoji == '👍':

            bye_hoe = em(
                title="You have been kicked from IsThicc Software!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            bye_hoe.add_field(
                name="Reason:",
                value=reason
            )
            bye_hoe.add_field(
                name="Kicked by:",
                value=ctx.author
            )
            bye_hoe.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            try:

                await member.send(embed=bye_hoe)
                await member.ban(reason=reason)

            except Exception:
                ohno = em(
                    title="Uh oh!",
                    description=f"Sorry! I couldn't kick {member.mention}! Please make sure I have proper permissions!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                )
                ohno.set_footer(
                    icon_url=self.avatar,
                    text="IsThicc Moderation"
                )
                return await msg.edit(embed=ohno)

            ded = em(
                title="Kicked!",
                description=f"I kicked {member} for {reason}!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            )
            ded.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            return await msg.edit(embed=ded)

        else:
            no = em(
                title=f"I won't kick {member}!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            )
            no.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            return await msg.edit(embed=no)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.has_role(744012353808498808)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def warn(self, ctx, member: discord.Member, reason, *):

        warned = em(
            title="You have been warned in IsThicc Software!",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        )
        warned.set_footer(
            icon_url=self.avatar,
            text="IsThicc Moderation"
        )
        ctx_warned = em(
            title="Warned!",
            description=f"I warned {member.mention} for {reason}!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        ctx_warned.set_footer(
            icon_url=self.avatar,
            text="IsThicc Moderation"
        )
        await ctx.send(embed=ctx_warned)
        await member.send(embed=warned)

        # TODO: Insert user id, datetime.now, and reason into warning db.
        #   #
        #   #   Tables:
        #   #       user_id
        #   #       reason
        #   #       time
        #   #
        #   # Psst, can you also do the magic insert if not whatever in database.py? Thank you for everything big bran fxc!

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.has_role(739510850079162530)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def unwarn(self, ctx, member: discord.Member):

        unwarned = em(
            title="Unwarned!",
            description=f"I removed the most recent warning for {member.mention}!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        unwarned.set_footer(
            icon_url=self.avatar,
            text="IsThicc Moderation"
        )
        await ctx.send(embed=unwarned)

        # TODO: Figure out how to unwarn someone but keep it in the db.

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @ban.error
    @kick.error
    @warn.error
    @unwarn.error
    async def mod_error(self, ctx, error):

        if isinstance(error, commands.MissingRole):
            oof = em(
                title="Missing Permissions!",
                description="Sorry! This command is only for staff members!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            oof.set_footer(
                icon_url=self.avatar,
                text="IsThicc"
            )
            await ctx.send(embed=oof)

        if isinstance(error, commands.MissingPermissions):
            no = em(
                title="Sorry! You don't have permission!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red()
            )
            no.set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            )
            return await ctx.send(embed=no)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(mod(bot))
