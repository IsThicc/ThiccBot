#
#           IsThicc-bot Staff.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio
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
        self.bot = bot
        self.session = ClientSession()

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(744012353808498808)
    async def staff(self, ctx, option = None, member = None):
        if option == None:
            rip = em(
                title="Uh Oh!",
                description="You haven't supplied a required argument!\nAvailable arguments:\n```view```\n_ _",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            rip.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            )
            return await ctx.send(embed=rip)

        if option == "view":
#             if not ctx.author.has_role(739510850079162530):
#                 noperms = em(
#                     title="You don't have permission!",
#                     description="Sorry! You don't have permission to execute this part!",
#                     colour=discord.Colour.red(),
#                     timestamp=datetime.utcnow()
#                 )
#                 noperms.set_footer(
#                     icon_url=self.bot.user.avatar_url,
#                     text="IsThicc Staff"
#                 )
#                 return await ctx.send(embed=noperms)

            if member is None:
                nomember = em(
                    title="You didn't supply a member!",
                    description="Oh no, you forgot to supply a member to check! Make sure you do that next time!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                )
                nomember.set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                return await ctx.send(embed=nomember)

            view = em(
                title=f"Attempting to view: {member}",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            )
            view.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            )
            msg = await ctx.send(embed=view)
            # TODO: Change this to aiohttp?
            request = await self.session.get(f"http://10.42.10.4:5000/staff/{member}")
            code = request.status_code
            await asyncio.sleep(2)

            if code == 200:
                response = request.json()
                yay = em(
                    title=f"Showing info for {member}",
                    description=f"Processed file: **``{response['details']['name']}.yml``**",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                )
                yay.add_field(
                    name="Position",
                    value="\n- ".join(response['details']['position'])
                )
                yay.add_field(
                    name="VPN IP",
                    value=response['details']['ip']
                )
                yay.add_field(
                    name="GitHub Access",
                    value="\n- ".join(response['details']['github_access'])
                )
                yay.add_field(
                    name="System Access",
                    value="\n- ".join(response['details']['system_access'])
                )
                yay.set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                request.close()
                return await msg.edit(embed=yay)

            elif code == 403:
                oof = em(
                    title="Oh no!",
                    description="You requested a staff member you're not allowed to access!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                )
                oof.set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                return await msg.edit(embed=oof)

            elif code == 404:
                no = em(
                    title="Unknown Staff Member!",
                    description="Your requested Staff Member does not exist!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                )
                no.set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                return await msg.edit(embed=no)
            else:
                uh = em(
                    title="U h",
                    description="You ran into an unknown response code! Make sure to report this to the developers!",
                    colour=discord.Colour.dark_red(),
                    timestamp=datetime.utcnow()
                )
                uh.set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                return await msg.edit(embed=uh)

        else:
            E = em(
                title="So uh, yea...",
                description="So you found this command! Good on you, just one issue, I haven't finished coding it! Make sure to yell at Mrmagicpie to finish this!",
                colour=discord.Colour.dark_red(),
                timestamp=datetime.utcnow()
            )
            E.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            )
            return await ctx.send(embed=E)




#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#


def setup(bot):
    bot.add_cog(staff_cog(bot))
