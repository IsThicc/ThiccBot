#
#                          IsThicc-bot Staff.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, re
from discord.ext          import commands, tasks
from discord.ext.commands import BucketType
from discord              import Embed as em
from datetime             import datetime
from aiohttp              import ClientSession
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Staff(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.session = ClientSession()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @tasks.loop(hours=24.0)
    async def deadline_route(self):

        # TODO: Make this into a function and then call it every 24 hours and at bot ready
        
        r    = await self.session.get("http://10.42.10.4:5000/staff/deadlines")
        json = await r.json()

        for staff in json['staff']:

            if len(json['staff'][staff]['deadlines']) == 0: continue

            deadlines = []

            for deadline in json['staff'][staff]['deadlines']:

                if deadline[1] is None: continue
                if datetime.strftime(deadline[1], "%d-%m-%Y") != datetime.now().strftime("%d-%m-%Y"): continue

                deadlines.append(deadline)

            if len(deadlines) == 0: continue

            reminder_embed = em(
                title="Development Reminders!",
                colour=discord.Colour.blue(),
                description="Hey! We noticed you still have a todo marked as incomplete. If you have finished any of these please disregard.\n**Use ``i!todo`` to view your todos!**",
                timestamp=datetime.utcnow()
            )

            for deadline in deadlines:
                reminder_embed.add_field(
                    name=f"Todo {deadline[0]}",
                    value=f"Todo #{str(deadline[0])} is due today - {datetime.strftime(deadline[1], '%d-%m-%Y')}!"
                )

            channel = discord.utils.get(self.bot.get_channel(812422468102520863).text_channels,
                                        name=staff.lower()[:-4])

            reminder_embed.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            )

            if channel is None:
                return await self.bot.get_channel(824848581609127998).send(embed=reminder_embed)

            return await channel.send(embed=reminder_embed)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.group(name="staff")
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(744012353808498808)
    async def staff(self, ctx):

        if ctx.invoked_subcommand is not None: return

        # option = None
        # member = None
        # try:

        return await ctx.send(embed=em(
            title="Uh Oh!",
            description="You haven't supplied a required argument!\nAvailable arguments:\n```view```\n_ _",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Staff"
        ))

        # return await ctx.send(embed=em(
        #     title="So uh, yea...",
        #     description="So you found this command! Good on you, just one issue, I haven't finished coding it! Make sure to yell at Mrmagicpie to finish this!",
        #     colour=discord.Colour.dark_red(),
        #     timestamp=datetime.utcnow()
        # ).set_footer(
        #     icon_url=self.bot.user.avatar_url,
        #     text="IsThicc Staff"
        # ))

        # except Exception as e:
        #     err_em = em(
        #         title="Command Error!",
        #         description=f"```py\n{e}```",
        #         colour=discord.Colour.red(),
        #         timestamp=datetime.utcnow()
        #     ).set_footer(
        #             icon_url=self.bot.user.avatar_url,
        #             text="IsThicc Staff"
        #     )
        #     if 'msg' in locals():
        #         return await locals()["msg"].edit(embed=err_em)
        #     else:
        #         return await ctx.send(embed=err_em)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @staff.command(name="strike")
    @commands.has_role(739510850079162530)
    async def strike(self, ctx, member: discord.Member = None, reason: str = "Lack of development."):

        if discord.Member is None:
            return await ctx.send(embed=em(
                title="Please provide a staff member!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

        self.bot.get_command(name="strike").__call__(ctx=ctx, member=member, reason=reason)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @staff.command(name="edit")
    async def edit(self, ctx, member: discord.Member = None):

        return await ctx.send(embed=em(
            title="This option is under development!",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Staff"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @staff.command(name="view")
    async def view(self, ctx, member: str = None):

        if member is None:
            return await ctx.send(embed=em(
                title="You didn't supply a member!",
                description="Oh no, you forgot to supply a member to check! Make sure you do that next time!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))
        else:

            discord_member = discord.utils.get(ctx.guild.members, name=member.split("#")[0])

            if discord_member is not None:
                msg = await ctx.send(embed=em(
                    title=f"Attempting to view: {discord_member.display_name}",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))
                member = str(discord_member.id)

            if member.startswith("<@"):
                member = re.search(r'(?<=<[!|@]|@!)\d+(?=>)', member)[0]

            msg = await ctx.send(embed=em(
                title=f"Attempting to view: {member}",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            ))

            request = await self.session.get(f"http://10.42.10.4:5000/staff/{member}")
            code = request.status

            if code == 200:

                response = await request.json()
                # github_r = await self.session.get(f"https://api.github.com/users/{response['details']['github_username']}")
                # github_code = github_r.status
                await asyncio.sleep(2)

                positions = []
                for position in response['details']['position']:
                    positions.append(f'- {position}')

                github = []
                for access in response['details']['github_access']:
                    github.append(f'- {access}')

                sysaccess = []
                for access in response['details']['system_access']:
                    sysaccess.append(f'- {access}')

                pronouns = []

                if len(response['details']['pronouns']) == 0:
                    pronouns.append("Not specified.")

                for pronoun in response['details']['pronouns']:
                    pronouns.append(f'- {pronoun}')

                staff = em(
                    title=f"Showing info for {response['details']['name'].capitalize()}",
                    description=f"Processed file: **``{response['details']['name']}.yml``**",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                )
                staff.set_thumbnail(
                    url=self.bot.get_user(response['details']['discord_id']).avatar_url
                )
                staff.add_field(
                    name="VPN IP",
                    value=response['details']['ip']
                )
                # staff.add_field(
                #     name="Twitter",
                #     value=twitter
                # )
                #
                # if github_response['hireable'] == True: hire = "Yes!"
                # else: hire = "Not currently!"
                # staff.add_field(
                #     name="Open to commissions?",
                #     value=hire
                # )
                #
                # if github_response['blog'] is None or len(github_response['blog']) == 0 or github_response['blog'] == "":
                #     site = "No Website on GitHub!"
                # else: site = github_response['blog']
                # staff.add_field(
                #     name="Website",
                #     value=site
                # )
                #
                # if github_response['company'] is not None:
                #     if github_response['company'].startswith("@"):
                #         try: company = f'[{github_response["company"].replace("@", "")}](https://github.com/{github_response["company"].replace("@", "")})'
                #         except: company = github_response['company']
                #     else:
                #         company = github_response['company']
                # else: company = "No Company on GitHub!"
                # staff.add_field(
                #     name="Company",
                #     value=company
                # )

                staff.add_field(
                    name="Position",
                    value="\n".join(positions)
                )
                staff.add_field(
                    name="Pronouns",
                    value="\n".join(pronouns)
                )
                staff.add_field(
                    name="System Access",
                    value="\n".join(sysaccess)
                )
                staff.add_field(
                    name="GitHub Access",
                    value="\n".join(github)
                )

                staff.set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                request.close()
                # github_r.close()

                return await msg.edit(embed=staff)

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
                    description=f"You ran into an unknown response code! Make sure to report this to the developers!\nExited with code `{str(code)}`",
                    colour=discord.Colour.dark_red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @staff.error
    async def staff_error(self, ctx, error):

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
    bot.add_cog(Staff(bot))
