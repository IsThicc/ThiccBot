#
#                          IsThicc-bot Staff.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, typing
from discord.ext import commands
from discord.ext.commands import BucketType
from discord import Embed as em
from datetime import datetime
from aiohttp import ClientSession
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class staff_cog(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session = ClientSession()

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(744012353808498808)
    async def staff(self, ctx, option=None, member: str = None):
        try:

            # if type(member) == str:
            #     member = discord.utils.get(ctx.guild.members, name=member)

            if option == None:
                return await ctx.send(embed=em(
                    title="Uh Oh!",
                    description="You haven't supplied a required argument!\nAvailable arguments:\n```view```\n_ _",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

            if option == "view":
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
                    return
                if member.startswith("<@"):
                    member = member.replace("<@", "").replace("!", "").replace(">", "") # ! isnt always there
                else:
                    member = str(discord_member.id)

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
                        github_r = await self.session.get(f"https://api.github.com/users/{response['details']['github_username']}")
                        github_code = github_r.status
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
                        staff.add_field(
                            name="Discord User",
                            value=self.bot.get_user(response['details']['discord_id']).mention
                        )
                        staff.add_field(
                            name="GitHub Access",
                            value="\n".join(github)
                        )
                        staff.add_field(
                            name="GitHub ID",
                            value=response['details']['github_id']
                        )
                        staff.add_field(
                            name="GitHub Username",
                            value=f"[{response['details']['github_username']}](https://github.com/{response['details']['github_username']})"
                        )

                        if github_code == 200:

                            github_response = await github_r.json()

                            if github_response['twitter_username'] is not None: twitter = github_response['twitter_username']
                            else: twitter = "No Twitter on GitHub!"
                            staff.add_field(
                                name="Twitter",
                                value=twitter
                            )

                            if github_response['hireable'] == True: hire = "Yes!"
                            else: hire = "Not currently!"
                            staff.add_field(
                                name="Open to commissions?",
                                value=hire
                            )

                            if github_response['blog'] is None or len(github_response['blog']) == 0 or github_response['blog'] == "":
                                site = "No Website on GitHub!"
                            else: site = github_response['blog']
                            staff.add_field(
                                name="Website",
                                value=site
                            )

                            if github_response['company'] is not None:
                                if github_response['company'].startswith("@"):
                                    try: company = f'[{github_response["company"].replace("@", "")}](https://github.com/{github_response["company"].replace("@", "")})'
                                    except: company = github_response['company']
                                else:
                                    company = github_response['company']
                            else: company = "No Company on GitHub!"
                            staff.add_field(
                                name="Company",
                                value=company
                            )

                        staff.add_field(
                            name="Position",
                            value="\n".join(positions)
                        )
                        staff.add_field(
                            name="System Access",
                            value="\n".join(sysaccess)
                        )

                        staff.set_footer(
                            icon_url=self.bot.user.avatar_url,
                            text="IsThicc Staff"
                        )
                        request.close()
                        github_r.close()

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
                            description="You ran into an unknown response code! Make sure to report this to the developers!",
                            colour=discord.Colour.dark_red(),
                            timestamp=datetime.utcnow()
                        ).set_footer(
                            icon_url=self.bot.user.avatar_url,
                            text="IsThicc Staff"
                        ))

            elif option == "edit":
                return await ctx.send(embed=em(
                    title="This option is under development!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

            else:
                return await ctx.send(embed=em(
                    title="So uh, yea...",
                    description="So you found this command! Good on you, just one issue, I haven't finished coding it! Make sure to yell at Mrmagicpie to finish this!",
                    colour=discord.Colour.dark_red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

        except Exception as e:
            print(e)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
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
            print(str(error))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(staff_cog(bot))
