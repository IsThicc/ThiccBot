#
#                          IsThicc-bot TODO.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, re, traceback
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

                request = await self.session.get(f"http://10.42.10.4:5000/staff/todo/{ctx.author.id}")
                code = request.status
                await asyncio.sleep(2)

                if code == 200:

                    json = await request.json()

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
                    
            elif option == 'finish' or option == 'complete':
                
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
                    
                # Send Messages #
                msg = await ctx.send(embed=em(
                        title="Please supply your password!",
                        description="We need to confirm it's really you before we can mark your TODO as completed!Please check your dm's!",
                        colour=discord.Colour.dark_red(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Staff"
                    )
                )
                pass_r_msg = await ctx.author.send(embed=em(
                        title="Please send your password below!",
                        colour=discord.Colour.green(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Staff"
                    )
                )
                timeout = em(
                    title="Timed out!",
                    description="Next time please respond within the timout time!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                )
                
                # Try to get password
                try:
                    def pass_check(m):
                        return m.author == ctx.author and m.channel == ctx.author.dm_channel
                    pass_msg = await self.bot.wait_for("on_message", check=pass_check, timeout=60)
                except asyncio.TimeoutError:
                    await msg.edit(embed=timeout)
                    return await pass_r_msg.edit(embed=timeout)
                except:
                    return await msg.edit(embed=em(
                            title="An unknown error occurred!",
                            colour=discord.Colour.red(),
                            timestamp=datetime.utcnow()
                        ).set_footer(
                            icon_url=self.bot.user.avatar_url,
                            text="IsThicc Staff"
                        )
                    )
                
                await pass_msg.reply(ping=False, embed=em(
                        title="Please delete your password!",
                        colour=discord.Colour.green(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Staff"
                    )
                )

                # Execute Request
                headers = {
                    "Authorization" : pass_msg.content,
                    "id" : extra
                }
                request = await self.session.get(f"http://10.42.10.4:5000/staff/todo/complete/{ctx.author.id}", headers=headers)
                code = request.status
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
                        )
                    )
                
                elif code == 500:
                    return await ctx.author.send(embed=em(
                            title="Uh oh!",
                            description="Oh no, the Backend API has responded with 500! Please tell IsThicc Management!",
                            colour=discord.Colour.red(),
                            timestamp=datetime.utcnow()
                        ).set_footer(
                            icon_url=self.bot.user.avatar_url,
                            text="IsThicc Management"
                        )
                    )
                
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
        except Exception as e:
            print(traceback.format_exc())
            err_em = em(
                title="Staff command error!",
                description=f"```py\n{e}```",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
            )
            if 'msg' in locals():
                return await locals()["msg"].edit(embed=err_em)
            else:
                return await ctx.send(embed=err_em)


#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(todo_cog(bot))
