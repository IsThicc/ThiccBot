#
#                          IsThicc-bot TODO.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, re, traceback
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

class Todo(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session = ClientSession()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def view_todo(self, ctx):
        msg = await ctx.send(embed=em(
            title=f"Attempting to view TODOs for {ctx.author.name}!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Staff"
        ))

        request = await self.session.get(f"http://10.42.10.4:5000/staff/todo/{ctx.author.id}")
        code    = request.status
        await asyncio.sleep(2)

        if code == 200:

            json = await request.json()

            staff = em(
                title=f"Showing info for {json['details']['name'].capitalize()}",
                description=f"Processed file: **``{json['details']['name']}.yml``**",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            )
            for count, todo in enumerate(json['todo']):
                TODO = json['todo'][todo]
                if count == 24:
                    staff.add_field(
                        name="Uh oh!",
                        value="You have more than 24 TODO's! Please check with a member of management!"
                    )
                    break
                else:
                    if len(TODO['description']) >= 1500:
                        TODO['description'] = "Please contact management! This description is over 1500 characters!"

                    if TODO['deadline'] is not None:
                        date = datetime.strptime(TODO['deadline'], '%d-%m-%Y').strftime('%A %B %d')
                    else:
                        date = "Not specified - Contact management if you need clarification!"

                    staff.add_field(
                        name=f"TODO #{TODO['id']}",
                        value=f"**Name:** {TODO['name']}\n**Description:** {TODO['description']}\n**Deadline:** {date}"
                    )

            staff.set_thumbnail(
                url=self.bot.get_user(json['details']['discord_id']).avatar_url
            )
            staff.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            )

            return await msg.edit(embed=staff)

        elif code == 204:
            request.close()
            return await msg.edit(embed=em(
                title="You have no TODO's!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

        elif code == 403:
            request.close()
            return await msg.edit(embed=em(
                title="Oh no!",
                description="You requested a staff member you're not allowed to access!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

        elif code == 404:
            request.close()
            return await msg.edit(embed=em(
                title="Unknown Staff Member!",
                description="Your requested Staff Member does not exist!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

        else:
            request.close()
            return await msg.edit(embed=em(
                title="U h",
                description=f"You ran into an unknown response code! Make sure to report this to the developers!\nExited with code `{code}`",
                colour=discord.Colour.dark_red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.group(name="todo", aliases=["t", "td"])
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(744012353808498808)
    async def todo(self, ctx):

        if ctx.invoked_subcommand is not None: return

        return await self.view_todo(ctx)

        # return await ctx.send(embed=em(
        #     title="Uh Oh!",
        #     description="You haven't supplied a required argument!\nAvailable arguments:\n```view```\n_ _",
        #     colour=discord.Colour.red(),
        #     timestamp=datetime.utcnow()
        # ).set_footer(
        #     icon_url=self.bot.user.avatar_url,
        #     text="IsThicc Staff"
        # ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @todo.command(name="view")
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(744012353808498808)
    async def view(self, ctx):
        await self.view_todo(ctx)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @todo.command(name="update", aliases=["updated"])
    @commands.has_role(739510850079162530)
    async def update(self, ctx, member: Union[discord.Member, str] = None):
        return await self.bot.get_command(name="updatetodo").__call__(ctx=ctx, member=member)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @todo.command(name="new")
    @commands.has_role(739510850079162530)
    async def new(self, ctx, member: Union[discord.Member, str] = None):
        return await self.bot.get_command(name="newtodo").__call__(ctx=ctx, member=member)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @todo.command(name="all")
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(739510850079162530)
    async def view_all(self, ctx):

        r    = await self.session.get("http://10.42.10.4:5000/staff/deadlines")
        json = await r.json()
        r_em = em(
            title="Viewing all TODOs!",
            description="This includes the date they're due and the ID along with the user's name.",
            colour=discord.Colour.blurple(),
            timestamp=datetime.utcnow()
        )

        for staff in json['staff']:

            # TODO: Add a check to make sure we don't go over the 25 field cap(if we ever have that many staff)
            if len(json['staff'][staff]['deadlines']) == 0: continue

            deadlines = []

            for deadline in json['staff'][staff]['deadlines']:

                if deadline[1] is None: continue
                # if deadline[1] != str(datetime.now().strftime("%d-%m-%Y")): continue

                deadlines.append(f"#{deadline[0]} - {datetime.strptime(deadline[1], '%d-%m-%Y').strftime('%A %B %d')}")

            if len(deadlines) == 0: continue

            r_em.add_field(
                name=staff.capitalize()[:-4],
                value="\n".join(deadlines)
            )

        r_em.set_thumbnail(url=ctx.guild.icon_url)
        r_em.set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        )

        return await ctx.send(embed=r_em)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @todo.command(name="finish", aliases=["complete"])
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(744012353808498808)
    async def finish(self, ctx, extra: str = None):

        if extra is None:
            return await ctx.send(embed=em(
                title="Yikes! You forgot to supply a TODO id!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

        if re.match("\D+", extra)!=None:
            return await ctx.send(embed=em(
                title="Oopsi! Your provided TODO contains chars that are not numbers!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

        msg = await ctx.send(embed=em(
            title="Attempting to mark your TODO as completed!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Staff"
        ))

        # # Send Messages #
        # msg = await ctx.send(embed=em(
        #     title="Please supply your password!",
        #     description="We need to confirm it's really you before we can mark your TODO as completed!Please check your dm's!",
        #     colour=discord.Colour.dark_red(),
        #     timestamp=datetime.utcnow()
        # ).set_footer(
        #     icon_url=self.bot.user.avatar_url,
        #     text="IsThicc Staff"
        # ))
        #
        # pass_r_msg = await ctx.author.send(embed=em(
        #     title="Please send your password below!",
        #     colour=discord.Colour.green(),
        #     timestamp=datetime.utcnow()
        # ).set_footer(
        #     icon_url=self.bot.user.avatar_url,
        #     text="IsThicc Staff"
        # ))
        #
        # timeout = em(
        #     title="Timed out!",
        #     description="Next time please respond within the timout time!",
        #     colour=discord.Colour.red(),
        #     timestamp=datetime.utcnow()
        # ).set_footer(
        #     icon_url=self.bot.user.avatar_url,
        #     text="IsThicc Staff"
        # )
        #
        # # Try to get password
        # try:
        #     def pass_check(m):
        #         return m.author == ctx.author and m.channel == ctx.author.dm_channel
        #     pass_msg = await self.bot.wait_for("on_message", check=pass_check, timeout=60)
        #
        # except asyncio.TimeoutError:
        #     await msg.edit(embed=timeout)
        #     return await pass_r_msg.edit(embed=timeout)
        #
        # except:
        #     return await msg.edit(embed=em(
        #         title="An unknown error occurred!",
        #         colour=discord.Colour.red(),
        #         timestamp=datetime.utcnow()
        #     ).set_footer(
        #         icon_url=self.bot.user.avatar_url,
        #         text="IsThicc Staff"
        #     ))
        #
        # await pass_msg.reply(ping=False, embed=em(
        #     title="Please delete your password!",
        #     colour=discord.Colour.green(),
        #     timestamp=datetime.utcnow()
        # ).set_footer(
        #     icon_url=self.bot.user.avatar_url,
        #     text="IsThicc Staff"
        # ))

        # Execute Request
        headers = {
            # TODO: Get bot Authorization from Config.py
            "Authorization": "",
            "id": extra
        }

        request = await self.session.get(f"http://10.42.10.4:5000/staff/todo/complete/{ctx.author.id}", headers=headers)
        code    = request.status

        await asyncio.sleep(2)

        # Handle Output
        request.close()
        if code == 200:
            await msg.edit(embed=em(
                title=f"Marked {ctx.author.display_name}'s TODO as completed!",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

        elif code == 403:
            return await ctx.author.send(
                embed=em(
                    title="Uh oh!",
                    description="Oh no, your provided password is not valid!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

        elif code == 500:
            return await ctx.author.send(embed=em(
                title="Uh oh!",
                description="Oh no, the Backend API has responded with 500! Please tell IsThicc Management!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        else:
            return await msg.edit(embed=em(
                title="U h",
                description=f"You ran into an unknown response code! Make sure to report this to the developers!\nExited with code `{code}`",
                colour=discord.Colour.dark_red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # @commands.command(name="todo", aliases=["t", "td"],)
    # @commands.cooldown(1, 1, BucketType.user)
    # @commands.has_role(744012353808498808)
    # async def todo(self, ctx, option=None, extra: str = None):
    #     try:
    #
    #         # if option == None:
    #         #     return await ctx.send(embed=em(
    #         #         title="Uh Oh!",
    #         #         description="You haven't supplied a required argument!\nAvailable arguments:\n```view```\n_ _",
    #         #         colour=discord.Colour.red(),
    #         #         timestamp=datetime.utcnow()
    #         #     ).set_footer(
    #         #         icon_url=self.bot.user.avatar_url,
    #         #         text="IsThicc Staff"
    #         #     ))
    #
    #         # option = option.lower()
    #
    #         if option == "view" or option == None:
    #
    #             if extra is not None:
    #                 return await ctx.send(embed=em(
    #                     title="This feature isn't supported yet!",
    #                     colour=discord.Colour.red(),
    #                     timestamp=datetime.utcnow()
    #                 ).set_footer(
    #                     icon_url=self.bot.user.avatar_url,
    #                     text="IsThicc Staff"
    #                 ))
    #
    #
    #
    #         elif option == 'finish' or option == 'complete':
    #
    #
    #
    #     except Exception as e:
    #         print(traceback.format_exc())
    #         err_em = em(
    #             title="Staff command error!",
    #             description=f"```py\n{e}```",
    #             colour=discord.Colour.red(),
    #             timestamp=datetime.utcnow()
    #         ).set_footer(
    #                 icon_url=self.bot.user.avatar_url,
    #                 text="IsThicc Staff"
    #         )
    #         if 'msg' in locals():
    #             return await locals()["msg"].edit(embed=err_em)
    #         else:
    #             return await ctx.send(embed=err_em)


    @todo.error
    async def todo_error(self, ctx, error):

        if isinstance(error, commands.MissingRole):
            await ctx.send(embed=em(
                title="Missing Permissions!",
                description="Sorry! This command is only for staff members!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))
        else:
            em_err = em(
                title="An error has occurred!",
                description=f"```css\n{str(error)}```",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            em_err.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            )

            if "msg" in locals():
                await locals()["msg"].edit(embed=em_err)
            else:
                await ctx.send(embed=em_err)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Todo(bot))
