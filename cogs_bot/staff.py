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
    async def staff(self, ctx, option=None, member: typing.Union[discord.Member, str] = None):

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
            print(member)
            if member == discord.Member:
                msg = await ctx.send(embed=em(
                    title=f"Attempting to view: {member.display_name}",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))
                member = member.id

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
                positions = []
                for position in response['details']['position']:
                    positions.append(f'- {position}')

                github = []
                for access in response['details']['github_access']:
                    github.append(f'- {access}')

                sysaccess = []
                for access in response['details']['system_access']:
                    sysaccess.append(f'- {access}')
                request.close()

                return await msg.edit(embed=em(
                    title=f"Showing info for {member}",
                    description=f"Processed file: **``{response['details']['name']}.yml``**",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                ).add_field(
                    name="Position",
                    value="\n".join(positions)
                ).add_field(
                    name="VPN IP",
                    value=response['details']['ip']
                ).add_field(
                    name="GitHub Access",
                    value="\n".join(github)
                ).add_field(
                    name="System Access",
                    value="\n".join(sysaccess)
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

            elif code == 403:
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
