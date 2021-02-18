#
#                          IsThicc-bot TODO.py | 2020-2021 (c) IsThicc
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

class todo_cog(commands.Cog):
    def __init__(self, bot):
        self.bot     = bot
        self.session = ClientSession()

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command(name="todo", aliases=["t", "td"],)
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(744012353808498808)
    async def todo(self, ctx, option=None, extra: str = None):
        try:

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

            option = option.lower()

            if option == "view":

                if extra is not None:
                    return await ctx.send(embed=em(
                        title="This feature isn't supported yet!",
                        colour=discord.Colour.red(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Staff"
                    ))

                msg = await ctx.send(embed=em(
                    title=f"Attempting to view TODOs for {ctx.author.name}!",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

                r = await self.session.get(f"http://10.42.10.4:5000/staff/todo/{ctx.author.id}")
                code = r.status
                await asyncio.sleep(2)

                if code == 200:

                    json = await r.json()

                    # {
                    #   "name": str
                    #   "info": str
                    #   "endpoint": str
                    #   "api_time": str/datetime
                    #   "todo":
                    #       {
                    #           1:
                    #               "name": str
                    #               "id": int
                    #               "description": str/None
                    #       }
                    #   "details":
                    #       {
                    #           "name": str
                    #           "discord_id": int
                    #       }
                    # }

                    staff = em(
                        title=f"Showing info for {json['details']['name'].capitalize()}",
                        description=f"Processed file: **``{json['details']['name']}.yml``**",
                        colour=discord.Colour.green(),
                        timestamp=datetime.utcnow()
                    )
                    for count, todo in enumerate(json['todo']):
                        TODO = json[todo]
                        if count == 24:
                            staff.add_field(
                                name="Uh oh!",
                                value="You have more than 24 TODO's! Please check with a member of management!"
                            )
                            break
                        else:
                            if len(TODO['description']) >= 1500:
                                TODO['description'] = "Please contact management! This description is over 1500 characters!"

                            staff.add_field(
                                name=f"TODO #{TODO['id']}",
                                value=f"**Name:** {TODO['name']}\n**Description:** {TODO['description']}"
                            )

                    staff.set_thumbnail(
                        url=self.bot.get_user(json['details']['discord_id'])
                    )
                    staff.set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Staff"
                    )

                    await self.bot.get_user(json['details']['discord_id']).send(embed=staff)
                    return await msg.edit(embed=em(
                        title="Data received - check your dms!",
                        colour=discord.Colour.green(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Staff"
                    ))

                elif code == 204:
                    r.close()
                    return await msg.edit(embed=em(
                        title="You have no TODO's!",
                        colour=discord.Colour.red(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Staff"
                    ))

                elif code == 403:
                    r.close()
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
                    r.close()
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
                    r.close()
                    return await msg.edit(embed=em(
                        title="U h",
                        description="You ran into an unknown response code! Make sure to report this to the developers!",
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
def setup(bot):
    bot.add_cog(todo_cog(bot))
