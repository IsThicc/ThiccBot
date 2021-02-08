#
#                          IsThicc-bot Staff.py | 2020-2021 (c) IsThicc
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
    async def staff(self, ctx, option=None):

        msg = await ctx.send(embed=em(
            title="Please supply your password!",
            description="This command requires extra system access! Please check your dms!",
            colour=discord.Colour.dark_red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        )
        )

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
                return m == ctx.author and m.channel == ctx.author.dm_channel

            message = await self.bot.wait_for("on_message", check=pass_check)

        except asyncio.TimeoutError:
            await msg.edit(embed=timeout)
            await pass_dm.edit(embed=timeout)

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

        await message.reply(ping=False, embed=em(
            title="Please delete your password!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        )
        )

        request = await self.session.get(f"http://10.42.10.4:5000/")  # TODO: Set this to request the backend API
        code = request.status
        await asyncio.sleep(2)

        # TODO: Finish this to process data and/or tell them no auth


#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
# @staff.error
# async def staff_error(self, ctx, error):
#     self.avatar = self.bot.user.avatar_url
#
#     if isinstance(error, commands.MissingRole):
#         oof = em(
#             title="Missing Permissions!",
#             description="Sorry! This command is only for staff members!",
#             colour=discord.Colour.red(),
#             timestamp=datetime.utcnow()
#         )
#         oof.set_footer(
#             icon_url=self.avatar,
#             text="IsThicc"
#         )
#         await ctx.send(embed=oof)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(staff_cog(bot))
