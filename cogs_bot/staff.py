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
                member = discord_member.id

            elif member.startswith("<@"):
                member = member.replace("<@!", "").replace(">", "")
                msg = await ctx.send(embed=em(
                    title=f"Attempting to view: {member}",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

            else:
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
            await asyncio.sleep(2)

            if code == 200:
                response = await request.json()
                github_r = await self.session.get(f"https://api.github.com/users/{response['details']['github_username']}")
                github_code = github_r.status
                print(github_code)
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
                    title=f"Showing info for {member}",
                    description=f"Processed file: **``{response['details']['name']}.yml``**",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                )
                staff.set_thumbnail(
                    url=self.bot.get_user(response['details']['discord_id']).avatar_url
                )
                staff.add_field(
                    name="Position",
                    value="\n".join(positions)
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
                staff.add_field(
                    name="System Access",
                    value="\n".join(sysaccess)
                )
                print('ded4')

                if github_code == 200:
                    print('ded3')
                    github_response = await github_r.json()
                    print(github_response)

                    if github_response['twitter_username'] is not None:
                        print('ded3-1-1')
                        twitter = github_response['twitter_username']
                    else:
                        print('ded3-1-2')
                        twitter = "No Twitter on GitHub!"
                    print('ded3-1')
                    staff.add_field(
                        name="Twitter",
                        value=twitter
                    )

                    if github_response['hireable'] == True:
                        hire = "Yes!"
                        print('ded3-2-1')
                    else:
                        print('ded3-2-2')
                        hire = "Not currently!"
                    print('ded3-2')
                    staff.add_field(
                        name="Open to commissions?",
                        value=hire
                    )

                    if github_response['blog'] is not None or github_response['blog'] != "":
                        site = github_response['blog']
                        print('ded3-3-1')
                    else:
                        print('ded3-3-2')
                        site = "No Website on GitHub!"
                    print('ded3-3')
                    staff.add_field(
                        name="Website",
                        value=site
                    )

                    if github_response['company'] is not None:
                        print('ded3-4-1')
                        if github_response['company'].startswith("@"):
                            print('ded3-4-2')
                            try: company = f'[{github_response.replace("@", "")}](https://github.com/{github_response.replace("@", "")})'
                            except: print('eeeeeeeeeeeeeeeeeeeeeee')
                        else:
                            print('ded3-4-3')
                            company = github_response['company']
                    else:
                        print('ded3-4-4')
                        company = "No Company on GitHub!"
                    print('ded3-4')
                    staff.add_field(
                        name="Company",
                        value=company
                    )

                print('ded1')

                staff.set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                print('ded')
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

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(staff_cog(bot))
