#
#                          IsThicc-bot Application.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, re
from discord.ext import commands
from discord.ext.commands import BucketType
from discord import Embed as em
from datetime import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
open_apps = {}
questions = []
class application_cog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
    @commands.command(name="application", aliases=["apply", "app"])
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(739510850079162530)
    async def application(self, ctx, option=None):
        try:
            if option == None:
                return await ctx.send(embed=em(
                    title="Uh Oh!",
                    description="You forgot to mention a user.",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

            # check for member
            if option.startswith("<@"):
                mid = re.search(r'(?<=<[!|@]|@!)\d+(?=>)', option)[0]
                member = discord.utils.get(ctx.guild.members, id=mid)
            else:
                member = discord.utils.get(ctx.guild.members, id=option.split("#")[0])
            if member == None:
                raise LookupError(f"No user with id/name `{option}` found!")
            
            if member.id in open_apps: del open_apps[member]

            # create channel and send message
            username = member.split("#")[0]
            channel = await self.bot.create_text_channel(f"application-{username}",category='806012160198705183')
            
            intro = await channel.send(embed=em(
                title="Thicc -Developer / Staff Support- Appliaction",
                url="https://isthicc.dev",
                description=f"Hello {member.mention}, welcome to your app!\nWhen you're ready, react with ✅ to start or ❌ to cancel, note: it will auto close in 1 minute.",
                colour=discord.Colour.gold(),
                timestamp=datetime.utcnow()
            ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
            ).set_thumbnail(
                url="https://isthicc.dev/assets/img/logo.png"
            ).set_author(
                name=username,
                url="https://isthicc.dev",
                icon_url=member.default_avatar_url
            ).add_field(
                name="Notes", 
                value="You will have limited time to reaspond to each question, make sure to check the footer of each embed question, there will be the time limit you'll have. This will auto close in 1 minute."
            ).add_field(
                name="-", 
                value="Good luck!"
            ))
            await intro.add_reaction('✅')
            await intro.add_reaction('❌')

            # add to queue / list
            open_apps[member.id] = {
                "message_id" : intro.id,
                "channel_id" : channel.id,
                "answers" : [],
            }
            
            # wait for confirmation
            try:
                def on_reaction(payload):
                    # if payload.member.id not in open_apps: return False
                    if str(payload.emoji) != '✅' and str(payload.emoji) != '❌':
                        return False
                    if open_apps[payload.member.id]["message_id"] != payload.message_id:
                        return False
                    return True
                payload = await self.bot.wait_for("on_raw_reaction_add", check=on_reaction, timeout=60)
            except asyncio.TimeoutError:
                if member.id in open_apps:
                    del open_apps[member.id]

                await channel.send(embed=em(
                    title="Closing Application",
                    url="https://isthicc.dev",
                    description=f"Your time expired, this app will close in 3 seconds.",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                ))
                asyncio.sleep(3)
                return await channel.delete()
            
            # if not accepted then delete the channel
            if str(payload.emoji) == '❌':
                await channel.send(embed=em(
                    title="Closing Application",
                    url="https://isthicc.dev",
                    description=f"You've decided to close this application, will close in 3 seconds..\nThanks for your interest in IsThicc and goodbye!",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                ))
                asyncio.sleep(3)
                return await channel.delete()

            # if not then proceed with the app *if not not accepted*

            return await channel.send(embed=em(
                    title="UwU",
                    url="https://isthicc.dev",
                    description=f"Yay it worked, No errors! 🎉",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                ))

        except Exception as e:
            return await ctx.send(embed=em(
                title="Ou u dumbass HenBOMB there's an error!",
                description=f"```py\n{e}```",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
            ))

    @commands.Cog.listener()
    async def on_message(message):

        pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        return
        if payload.member.id not in open_apps: return
        if open_apps[payload.member.id]["message_id"] != payload.message_id: return
        channel = self.bot.get_channel(806012160198705183)

        if str(payload.emoji) == "✅":

            pass
        elif str(payload.emoji) == "❌":

            pass
            
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(application_cog(bot))
