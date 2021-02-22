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
    async def announce(self, ctx, option=None):

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
        code = request.status
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

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
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

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command()
    @commands.has_role(744012353808498808)
    async def archive(self, ctx):

        await ctx.message.delete()
        await ctx.send(embed=em(
            title="IsThicc Management will be archiving this channel shortly!",
            colour=discord.Colour.blue(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command()
    @commands.has_role(744012353808498808)
    async def accept(self, ctx, member: discord.Member):

        await ctx.message.delete()
        await ctx.send(content=member.mention, embed=em(
            title="Welcome to the team!",
            description="Welcome to the IsThicc team! You will be on a one week trial period. During this one week period you will have almost all the same permissions as a normal staff member. At the end of the 1 week, the board will decide if your position will become permanent.\n_ _\nThank you for applying!\n**IsThicc Management**\n_ _",
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text="IsThicc Management"
        ))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(staff_cog(bot))
