#
#                         IsThicc-bot Management.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, subprocess
from discord.ext          import commands
from discord.ext.commands import BucketType
from discord              import Embed as em
from datetime             import datetime
from aiohttp              import ClientSession
from typing               import Union
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Management(commands.Cog):
    def __init__(self, bot):
        self.bot      =  bot
        self.session  =  ClientSession()

    role = 739510850079162530
    help = "An IsThicc Sotware Management commmand."

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="announce", help=help)
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(role)
    async def announce(self, ctx, option=None):

        msg = await ctx.send(embed=em(
            title="Please supply your password!",
            description="This command requires extra system access! Please check your dms!",
            colour=discord.Colour.dark_red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

        timeout = em(
            title="Timed out!",
            description="Next time please respond within the timout time!",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        )

        try:
            pass_dm = await ctx.author.send(embed=em(
                title="Please send your password below!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            )
            )

            def pass_check(m):
                return m.author == ctx.author and m.channel == ctx.author.dm_channel

            message = await self.bot.wait_for("on_message", check=pass_check)

        except asyncio.TimeoutError:
            await msg.edit(embed=timeout)
            return await pass_dm.edit(embed=timeout)

        except:
            return await msg.edit(embed=em(
                title="An unknown error occurred!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        await message.reply(ping=False, embed=em(
            title="Please delete your password!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

        request = await self.session.post(f"http://10.42.10.4:5000/token/{message.content}")
        code = request.status
        await asyncio.sleep(2)

        if code == 403:
            return await ctx.author.send(
                embed=em(
                    title="Uh oh!",
                    description="Oh no, your provided password is not valid!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                )
            )

        elif code == 500:
            return await ctx.author.send(
                embed=em(
                    title="Uh oh!",
                    description="Oh no, the Backend API has responded with 500! Please tell IsThicc Management!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                )
            )

        try:
            # Service
            service_dm = await ctx.author.send(embed=em(
                title="Please send your service below(all, specific name)!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

            def service_check(m):
                return m.author == ctx.author and m.channel == ctx.author.dm_channel

            service = await self.bot.wait_for("on_message", check=service_check)

        except asyncio.TimeoutError:
            await msg.edit(embed=timeout)
            return await service_dm.edit(embed=timeout)

        except:
            return await msg.edit(embed=em(
                title="An unknown error occurred!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            )
            )

        try:
            # Announcement
            announce_dm = await ctx.author.send(embed=em(
                title="Please send your announcement below!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            )
            )

            def announce_check(m):
                return m.author == ctx.author and m.channel == ctx.author.dm_channel

            announcement = await self.bot.wait_for("on_message", check=announce_check)

        except asyncio.TimeoutError:
            await msg.edit(embed=timeout)
            return await announce_dm.edit(embed=timeout)

        except:
            return await msg.edit(embed=em(
                title="An unknown error occurred!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        try:
            # Type
            type_dm = await ctx.author.send(embed=em(
                title="What type do you want to send(webhook, email)!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

            def announce_check(m):
                return m.author == ctx.author and m.channel == ctx.author.dm_channel

            announce_type = await self.bot.wait_for("on_message", check=announce_check)

        except asyncio.TimeoutError:
            await msg.edit(embed=timeout)
            return await type_dm.edit(embed=timeout)

        except:
            return await msg.edit(embed=em(
                title="An unknown error occurred!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            )
            )

        request = await self.session.post(f"http://10.42.10.4:5000/announce/{announce_type.content}/{service.content}",
                                          headers={
                                              "Authorization": message.content,
                                              "content": announcement.content
                                          })
        code     = request.status
        response = await request.json()

        if code != 200:
            await msg.edit(
                embed=em(
                    title="Uh oh!",
                    description="An internal error has occurred! Please check your dms!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                )
            )

            return await ctx.author.send(
                embed=em(
                    title="Oh no!",
                    description=f"""
**Error:**
```css
{response}```
                    """,
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                )
            )

        return await ctx.author.send(
            embed=em(
                title="Success!",
                description=f"You have sent your announcement to {service.content}!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            )
        )

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @announce.error
    async def staff_error(self, ctx, error):

        if isinstance(error, commands.MissingRole):
            return await ctx.send(embed=em(
                title="Missing Permissions!",
                description="Sorry! This command is only for staff members!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        else: print(str(error))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="archive", help=help)
    @commands.has_role(role)
    async def archive(self, ctx):

        await ctx.message.delete()
        await ctx.send(embed=em(
            title="IsThicc Management will be archiving this channel shortly!",
            colour=discord.Colour.blue(),
            timestamp=datetime.utcnow()
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="accept", help=help)
    @commands.has_role(role)
    async def accept(self, ctx, member: discord.Member):

        if member is None:

            await ctx.message.delete()
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Uh oh, you forgot to supply an additional argument. Please make sure to supply a member.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        await ctx.message.delete()
        await ctx.send(content=member.mention, embed=em(
            title="Welcome to the team!",
            description="Welcome to the IsThicc team! You will be on a one week trial period. During this one week period you will have almost all the same permissions as a normal staff member. At the end of the 1 week, the board will decide if your position will become permanent.\n_ _\nThank you for applying!\n**IsThicc Management**\n_ _",
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="remind", help=help)
    @commands.has_role(role)
    async def remind(self, ctx, option="development", member: discord.Member = None):

        if option is None or member is None:

            await ctx.message.delete()
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Uh oh, you forgot to supply an additional argument. Please make sure to supply a member and option.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).add_field(
                name="Options:",
                value="```css\ndevelopment\n```"
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        if option.lower() == "development":

            await ctx.message.delete()
            return await ctx.send(content=member.mention, embed=em(
                title="IsThicc Management",
                description=f"""
Hey {member.mention}, we noticed you haven't been making any progress. Please let us know how we can help you! If you cannot make any progress for any reason, make sure to let us know!

**This message has been sent based on Git commits.**
<#794454957440892930>
                """,
                colour=discord.Colour.dark_red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        else:

            await ctx.message.delete()
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Uh oh, you gave an undefined argument! Please make sure to supply a valid member and option.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).add_field(
                name="Options:",
                value="```css\ndevelopment\n```"
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="strike", help=help)
    @commands.has_role(role)
    async def strike(self, ctx, member: discord.Member=None, *, reason="Lack of development."):

        if member is None:

            await ctx.message.delete()
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Uh oh, you forgot to supply an additional argument. Please make sure to supply a member *and maybe a reason*.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        await ctx.message.delete()
        return await ctx.send(content=member.mention, embed=em(
            title="IsThicc Management",
            description=f"""
Hello {member.mention},
We're sorry to say it but you have received a strike! 

A strike is a mark on your staff record. 3 strikes will result in disciplinary action or loosing your position! This has been sent on behalf of the IsThicc Board of Operations. 

**Approved by the IsThicc Board of Operations on {datetime.now().strftime("%b %d, %Y")}**
            """,
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).add_field(
            name="Reason:",
            value=reason
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="reload", help=help)
    @commands.is_owner()
    async def reload(self, ctx, cog: str = None):
        msg = await ctx.send(embed=discord.Embed(description="GitHub Pulling...", colour=discord.Colour.green()))
        await asyncio.sleep(1)
        
        res = subprocess.getoutput("git pull https://github.com/IsThicc/IsThicc-Bot")
        await msg.edit(embed=discord.Embed(description=f"Pulled from GitHub...\n```{res}```", colour=discord.Colour.green()))
        await asyncio.sleep(1)
        
        await msg.edit(embed=discord.Embed(description="Reloading cog...", colour=discord.Colour.red()))
        await asyncio.sleep(1)
        
        self.bot.reload_extension(f'cogs.{cog}')
        
        await msg.edit(embed=discord.Embed(description=f"Reloaded cog **{cog}**!", colour=discord.Colour.green()))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def new_todo_embed(self, member, channel, ctx):
        return await channel.send(content=member.mention, embed=em(
            title="IsThicc Management",
            description=f"""
Hey {member.mention}, 

You have new TODO's! Please make sure to review them!
``{ctx.prefix}todo view``
            """,
            colour=discord.Colour.dark_magenta(),
            timestamp=datetime.utcnow()
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def update_todo_embed(self, member, channel, ctx):
        return await channel.send(content=member.mention, embed=em(
            title="IsThicc Management",
            description=f"""
Hey {member.mention}, 

Your TODOs have been **updated**! Please make sure to review them!
``{ctx.prefix}todo view``
            """,
            colour=discord.Colour.blue(),
            timestamp=datetime.utcnow()
        ).set_thumbnail(
            url=ctx.guild.icon_url
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="wireguard", aliases=["wg", "vpn"], help=help)
    @commands.has_role(role)
    async def wireguard(self, ctx, member: Union[discord.Member] = None):

        if member is None:
            await ctx.message.delete()
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Uh oh, you forgot to supply an additional argument. Please make sure to supply a member.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        return await ctx.send(content=member.mention, embed=em(
            title="Wireguard!",
            description=f"""
Hey {member.mention}, IsThicc Management believe you are ready to get Wireguard access! Wireguard is a VPN client that we use to let staff use our internal services. 

Please follow the instructions in <#800601043346915369> to get ready. If you have any concerns or issues with this please let us know! Once you've made it to the end please wait for Management!
""",
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="newtodo", aliases=["new_todo", "nt", "ntodo"], help=help)
    @commands.has_role(role)
    async def newtodo(self, ctx, member: Union[discord.Member, str] = None):

        if member is None:

            await ctx.message.delete()
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Uh oh, you forgot to supply an additional argument. Please make sure to supply a member.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        if type(member) is not discord.Member:
            if member != "all":
                await ctx.message.delete()
                return await ctx.author.send("You inputted an incorrect argument! Please yell at Pie to finish this with an embed!")

            staff_dict = {}
            for staff in ctx.guild.get_role(744012353808498808).members:
                staff_dict[staff.name.lower()] = staff

            #                               Staff development category
            for channel in self.bot.get_channel(812422468102520863).channels:
                if channel.name in staff_dict:
                    await self.new_todo_embed(staff_dict[channel.name], channel, ctx)
            return

        await ctx.message.delete()
        return await self.new_todo_embed(member, ctx.channel, ctx)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="updatetodo", help=help)
    @commands.has_role(role)
    async def updatetodo(self, ctx, member: Union[discord.Member, str] = None):

        if member is None:

            await ctx.message.delete()
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Uh oh, you forgot to supply an additional argument. Please make sure to supply a member.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_thumbnail(
                url=ctx.guild.icon_url
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        if type(member) is not discord.Member:
            if member != "all":
                await ctx.message.delete()
                return await ctx.author.send("You inputted an incorrect argument! Please yell at Pie to finish this with an embed!")

            staff_dict = {}
            for staff in ctx.guild.get_role(744012353808498808).members:
                staff_dict[staff.name.lower()] = staff

            #                               Staff development category
            for channel in self.bot.get_channel(812422468102520863).channels:
                if channel.name in staff_dict:
                    await self.update_todo_embed(staff_dict[channel.name], channel, ctx)

        await ctx.message.delete()
        return await self.update_todo_embed(member, ctx.channel, ctx)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def check_api(self, admin: bool = None) -> dict:
        r      = await self.session.get("http://127.0.0.1:5000/endpoints")
        j      = await r.json()
        d      = j['details']
        r_dict = {}

        for e in d:
            if admin:
                r_dict[e] = d[e]

            elif not admin:
                if d[e]['admin']: continue
                r_dict[e] = d[e]

            elif admin is None:
                if d[e]['admin'] or d[e]['staff']: continue
                r_dict[e] = d[e]

        r.close()
        return r_dict

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def api_member(self, ctx):
        return await ctx.send(embed=em(
            title="Oh no!",
            description="Sorry! This command is currently only available for Staff members!",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management!"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def api_staff(self, ctx):

        ...

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def api_management(self, ctx):

        request = await self.session.get("http://10.42.10.4:5000/endpoints")
        json    = await request.json()

        if request.status != 200 or 'details' not in json:
            return await ctx.send(embed=em(
                title="An API Error has occurred!",
                description=f"Please check logs to figure out why a {request.status} has happened!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc API Management"
            ))

        msg = await ctx.send(embed=em(
            title="Processing request!",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc API Management"
        ))

        r_em = em(
            title="Management API Urls!",
            description="Below are the API endpoints available for Management, Staff and normal user use.",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )

        if len(json['details']) <= 25:
            for endpoint in json['details']:
                r_em.add_field(
                    name=endpoint['route'],
                    value=f"""
**Authorization:**
Admin: {endpoint['admin']}
Staff: {endpoint['staff']}

**Methods:**
``{"`` | ".join(endpoint['methods'])}``
                    """
                )

        else:
            for endpoint in json['details']: ...

        await msg.edit(embed=r_em)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="api", aliases=["apis"], help=help)
    async def api(self, ctx):

        # Staff
        if ctx.author.permissions_in(self.bot.get_channel(744010240542113792)).send_messages:
            return await self.api_staff(ctx)

        # Management
        elif ctx.author.permissions_in(self.bot.get_channel(744010240542113792)).send_messages:
            return await self.api_management(ctx)

        else:
            return await self.api_member(ctx)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Management(bot))
