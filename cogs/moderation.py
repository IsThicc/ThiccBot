#
#                          IsThicc-bot Moderation.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, random, string
from discord.ext import commands
from discord     import Embed as em
from discord     import Colour
from datetime    import datetime
from uuid        import uuid4
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db  = bot.db

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.has_guild_permissions(ban_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def ban(self, ctx, member: discord.Member, *, reason = "Banned from IsThicc Software"):
        self.avatar = self.bot.user.avatar_url

        # lets_make_sure = em(
        #     title=f"Are you sure you want to ban {member.display_name}?",
        #     colour=discord.Colour.dark_red(),
        #     timestamp=datetime.utcnow()
        # )
        # lets_make_sure.set_footer(
        #     icon_url=self.avatar,
        #     text="IsThicc Moderation"
        # )
        # msg = await ctx.send(embed=lets_make_sure)
        # await msg.add_reaction('👍')
        # await msg.add_reaction('👎')

        # try:
        #     print('e1')
        #     def yes_no(reaction, user):
        #         return user.id == ctx.author.id and reaction.channel.id == ctx.channel.id
        #     print('e2')
        #     # reaction, user = await self.bot.wait_for('reaction_add', check=yes_no) # , timeout=60)
        #     print('e')
        #
        #     reaction, user = await self.bot.user.wait_for('reaction_add', check=yes_no, timeout=60)
        #
        # except asyncio.TimeoutError:
        #
        #     timeout = em(
        #         title="Timed out!",
        #         description="You timed out! make sure to react within 60 seconds next time!",
        #         colour=discord.Colour.red(),
        #         timestamp=datetime.utcnow()
        #     )
        #     timeout.set_footer(
        #         icon_url=self.avatar,
        #         text="IsThicc Moderation"
        #     )
        #     await msg.clear_reactions()
        #     return await msg.edit(embed=timeout)
        #
        # await msg.clear_reactions()
        # emoji = str(reaction)
        #
        # if emoji == '👍':

        if member.guild_permissions.ban_members:
            return await ctx.send(embed=em(
                title="Sorry!",
                description="Sorry! I'm not able to ban this person as they also have ban permissions!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))

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
            return await ctx.send(embed=ohno)

        return await ctx.send(embed=em(
            title="Banned!",
            description=f"I banned {member} for {reason}!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.avatar,
            text="IsThicc Moderation"
        ))

        # else:
        #     return await msg.edit(embed=em(
        #         title=f"I won't ban {member}!",
        #         colour=discord.Colour.green(),
        #         timestamp=datetime.utcnow()
        #     ).set_footer(
        #         icon_url=self.avatar,
        #         text="IsThicc Moderation"
        #     ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def warn(self, ctx, m: discord.Member = None, reason: str = 'No reason specified.'):
        if m is None:
            return await ctx.reply('You didnt specify a member! Usage:\n`warn <member> <reason>')
        
        _id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        
        await self.db.execute("INSERT INTO warnings VALUES('" + str(_id) + "','" + str(m.id) + "')")
        e = em(description=f'I have warned {m.mention} for the reason **{reason}** with the warn id: `{_id}`', colour=Colour.teal(), timestamp=datetime.utcnow())
        await ctx.reply(embed=e)

        e2 = em(description=f'You got warned on **{ctx.guild}** by {ctx.author.mention} for the reason: **{reason}**\nWarn ID: `{_id}`', colour=Colour.red())
        await m.send(embed=e2)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(aliases=('delwarn',))
    @commands.has_guild_permissions(manage_roles=True)
    async def unwarn(self, ctx, m: discord.Member = None, warnid: str = None):
        if m is None or warnid is None:
            return await ctx.reply('You didnt specify a member to unwarn! Usage:\n`unwarn <member> <warn id>`')
         
        await self.db.execute("DELETE FROM warnings WHERE warn_id = '" + warnid + "'")
        e = em(description=f'I have removed the warning **{warnid}** from {m.mention}.', colour=Colour.green())
        await ctx.reply(embed=e)

        e2 = em(description=f'Your warning by the id **{warnid}** got removed by {ctx.author.mention}!', colour=Colour.teal())
        await m.send(embed=e2)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="mute")
    @commands.has_guild_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member = None, *, reason: str = "No reason specified."):
        if member is None:
            return await ctx.reply('You didnt specify a member! Usage:\n`mute <member>`')
        
        if member.guild_permissions.manage_roles:
            return await ctx.reply(embed=em(
                title="Sorry!",
                description="Sorry! I'm not able to mute this person as they also have manage roles permissions!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))
            
        if 748026204204040254 in [r.id for r in member.roles]:
            return await ctx.reply(f"{member} is already muted!")
        
        await member.add_roles(ctx.guild.get_role(748026204204040254))
        await member.send(f"You have been muted in **IsThicc Software** for **{reason}**!")
        await ctx.reply(f"Muted {member} for **{reason}**!")
    
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    @commands.command(name="unmute")
    @commands.has_guild_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member = None):
        if member is None:
            return await ctx.reply('You didnt specify a member! Usage:\n`unmute <member>`')
        
        if 748026204204040254 not in [r.id for r in member.roles]:
            return await ctx.reply(f"{member} is not muted!")
        
        await member.remove_roles(ctx.guild.get_role(748026204204040254))
        await ctx.reply(f"Unmuted {member}!")
        
    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.has_guild_permissions(manage_roles=True)
    async def warnings(self, ctx, m: discord.Member = None):
        if m is None:
            return await ctx.reply('You didnt specify a member to view warnings! Usage:\n`warnings <member>`')
        
        r = await self.db.execute('SELECT * FROM warnings WHERE user_id = ' + str(m.id) + '')

        warnings = []
        for i in range(len(r)):
            warnings.append(f'{i + 1} - {r[i][0]}')

        e = em(title=f'{m}(s) Warnings', colour=Colour.teal(), description='\n'.join(warnings), timestamp=datetime.utcnow())
        e . set_thumbnail(url=self.bot.user.avatar_url_as(format='png'))
        await ctx.reply(embed=e)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.has_guild_permissions(kick_members=True)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def kick(self, ctx, member: discord.Member, *, reason = "Kicked from IsThicc Software"):

        # lets_make_sure = em(
        #     title=f"Are you sure you want to kick {member.display_name}?",
        #     colour=discord.Colour.dark_red(),
        #     timestamp=datetime.utcnow()
        # )
        # lets_make_sure.set_footer(
        #     icon_url=self.bot.user.avatar_url,
        #     text="IsThicc Moderation"
        # )
        # msg = await ctx.send(embed=lets_make_sure)
        # await msg.add_reaction('👍')
        # await msg.add_reaction('👎')
        #
        # try:
        #
        #     def yes_no(reaction, user):
        #         return user.id == ctx.author.id and reaction.channel.id == ctx.channel.id
        #
        #     reaction, user = await self.bot.wait_for('reaction_add', check=yes_no, timeout=60)
        #
        # except asyncio.TimeoutError:
        #
        #     await msg.clear_reactions()
        #     return await msg.edit(embed=em(
        #         title="Timed out!",
        #         description="You timed out! make sure to react within 60 seconds next time!",
        #         colour=discord.Colour.red(),
        #         timestamp=datetime.utcnow()
        #     ).set_footer(
        #         icon_url=self.bot.user.avatar_url,
        #         text="IsThicc Moderation"
        #     ))

        # await msg.clear_reactions()
        # emoji = str(reaction)

        # if emoji == '👍':

        try:

            if member.guild_permissions.kick_members:
                return await ctx.send(embed=em(
                    title="Sorry!",
                    description="Sorry! I'm not able to kick this person as they also have kick permissions!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Moderation"
                ))

            await member.send(embed=em(
                title="You have been kicked from IsThicc Software!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).add_field(
                name="Reason:",
                value=reason
            ).add_field(
                name="Kicked by:",
                value=ctx.author
            ).set_footer(
                icon_url=self.avatar,
                text="IsThicc Moderation"
            ))
            await member.kick(reason=reason)

        except Exception:
            return await ctx.send(embed=em(
                title="Uh oh!",
                description=f"Sorry! I couldn't kick {member.mention}! Please make sure I have proper permissions!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))

        return await ctx.send(embed=em(
            title="Kicked!",
            description=f"I kicked {member} for {reason}!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Moderation"
        ))

        # else:
        #     return await msg.edit(embed=em(
        #         title=f"I won't kick {member}!",
        #         colour=discord.Colour.green(),
        #         timestamp=datetime.utcnow()
        #     ).set_footer(
        #         icon_url=self.bot.user.avatar_url,
        #         text="IsThicc Moderation"
        #     ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.has_role(744012353808498808)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def warn(self, ctx, member: discord.Member, *, reason = "No reason specified."):

        await ctx.send(embed=em(
            title="Warned!",
            description=f"I warned {member.mention} for {reason}!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Moderation"
        ))
        try:
            await member.send(embed=em(
                title="You have been warned in IsThicc Software!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))
        except:
            await ctx.author.send(embed=em(
                title=f"I was unable to send the warn message to {member}!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))

        # warn_id = "".join(random.choice(string.ascii_letters + string.digits) for _ in range(15))
        warn_id = str(uuid4())
        await self.db.warn(ctx.author.id, reason, datetime.utcnow(), True, warn_id)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.has_role(739510850079162530)
    @commands.cooldown(1, 1, commands.BucketType.user)
    @commands.command()
    async def unwarn(self, ctx, member: discord.Member, warnid: str):

        try:
            await self.db.unwarn(warnid)
            return await ctx.send(embed=em(
                title="Unwarned!",
                description=f"I removed the warning `{warnid}` for {member.mention}!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))
        except Exception as e:
            print(e)
            return await ctx.send(embed=em(
                title="Error!",
                description=f"An internal error has occurred! Sorry about this!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @ban.error
    @kick.error
    @warn.error
    @unwarn.error
    async def mod_error(self, ctx, error):

        if isinstance(error, commands.MissingRole):
            return await ctx.send(embed=em(
                title="Missing Permissions!",
                description="Sorry! This command is only for Staff members!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))

        if isinstance(error, commands.MissingPermissions):
            return await ctx.send(embed=em(
                title="Sorry! You don't have permission!",
                timestamp=datetime.utcnow(),
                colour=discord.Colour.red()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Moderation"
            ))

        else: print(str(error))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Moderation(bot))
