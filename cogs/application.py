#
#                          IsThicc-bot Application.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, traceback
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

# write dis shet
# time is in minutes
questions = {
    1 : {
        "time" : 5,
        "title" : "What are you applying for?",
        "description" : "Available positions:\n**Developer**: Help work on IsThicc's software and projects. and **Support Staff**.\n",
        "required": ["dev","developer","support","staff"]
    },
    2 : {
        "time" : 5,
        "title" : "Hoi",
        "description" : "You cant proceed unless you type 'uwu'",
        "required": ["uwu"]
    }
}

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
    async def application(self, ctx, member: discord.Member):
        try:
            if member == None:
                return await ctx.send(embed=em(
                    title="Uh Oh!",
                    description="You forgot to mention a user.\nUsage: `i!apply/app` `[ping/name]`",
                    colour=discord.Colour.red(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
                ))

            if member.id in open_apps: del open_apps[member.id]

            # create channel and send message
            category = discord.utils.get(ctx.guild.categories, name='『 Staff Development 』')
            channel = await ctx.guild.create_text_channel(f"application-{member.display_name}",category=category)
            await channel.set_permissions(member, send_messages=True, read_messages=True)
            await channel.set_permissions(ctx.guild.get_member(348547981253017610), send_messages=True, read_messages=True)

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
                    name=member.display_name,
                    url="https://isthicc.dev",
                    icon_url=member.avatar_url
                ).add_field(
                    name="Notes", 
                    value="You will have limited time to reaspond to each question, make sure to check the footer of each embed question, there will be the time limit you'll have. This will auto close in 1 minute.",
                    inline=False
                ).add_field(
                    name="-", 
                    value="Good luck!",
                    inline=False
                ))
            await intro.add_reaction('✅')
            await intro.add_reaction('❌')

            # add to open apps
            open_apps[member.id] = {
                "message_id" : intro.id,
                "channel_id" : channel.id,
                "answers" : {},
                "index" : 0
            }

            # wait for confirmation
            try:
                def on_reaction(reaction, user):
                    # if payload.member.id not in open_apps: return False
                    return (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌") and not user.bot and open_apps[user.id] and open_apps[user.id]["message_id"] == reaction.message.id
                reaction, user = await self.bot.wait_for("reaction_add", check=on_reaction, timeout=60)
            except asyncio.TimeoutError:
                if len(open_apps[member.id]["answers"])>0:
                    return

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
                await asyncio.sleep(3)
                return await channel.delete()
            
            # if not accepted then delete the channel
            if str(reaction.emoji) == '❌':
                if member.id in open_apps:
                    del open_apps[member.id]
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
                await asyncio.sleep(3)
                return await channel.delete()

            # if accepted then proceed with the questions

            
            # loop though questions and get answers
            for _ in range(len(questions)):
                open_apps[member.id]["index"] += 1
                # create array for answers
                open_apps[member.id]["answers"][open_apps[member.id]["index"]] = []
                # wait for the question to end
                code = await self.ask_question((ctx, member, channel))

                # code -> 0 = next question, 1 = quit, 2 = timeout
                if code == 1:
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
                elif code == 2:
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
                # else:
                #     await channel.send(embed=em(
                #         description=f"Onwards!",
                #         colour=discord.Colour.green(),
                #         timestamp=datetime.utcnow()
                #     ))

                if code == 1 or code == 2:
                    del open_apps[member.id]
                    await asyncio.sleep(3)
                    return await channel.delete()

            # when all the questions are answered
            await channel.send(embed=em(
                title="Thank You!",
                url="https://isthicc.dev",
                description="Your app will be reviewed and we'll get back to you!\nThanks for being interested in IsThicc Sofware.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))
            
            ans = open_apps[member.id]["answers"]
            await channel.send(embed=em(
                description=f"Just making sure lol:```py\n{ans}```",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))

        except Exception as e:
            print(traceback.format_exc())
            return await ctx.send(embed=em(
                title="Ou u dumbass HenBOMB there's an error!",
                description=f"```py\n{traceback.format_exc()}```",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
            ))

    # open_apps = {
    #   message_id:str,
    #   channel_id:str,
    #   answers:dict -> {1:[],2:[],...},
    #   index:int,
    # }
    # questions {
    #   1:{
    #       time:int,
    #       title:str, 
    #       description:str,
    #       required:list[str]
    #   }
    #   2:{...}, ...
    async def ask_question(self, vars):
        # setup
        ctx, member, channel = vars
        app = open_apps[member.id]
        index = app["index"]
        question = questions[index]
        time = question["time"] * 60

        # send message
        msg = await channel.send(embed=em(
            title=question["title"],
            url="https://isthicc.dev",
            description=question["description"] + "\nReact with ✅ to proceed with the next question or ❌ to stop the application.",
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"You have {time} minute(s) to answer"
        ).set_author(
            name=f"Question {index}",
            url="https://isthicc.dev",
            icon_url=member.default_avatar_url
        ))
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')

        # await for reaction
        # messages are automatically collected
        # wait_for_answers() returns a 0-3 code
        return await self.wait_for_answers((time, member.id, question, channel), msg)
    
    async def wait_for_answers(self, vars, message):
        time, id, question, channel = vars
        app = open_apps[id]

        try:
            def on_reaction(reaction, user):
                return (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌") and not user.bot and app["message_id"] == reaction.message.id
            reaction, user = await self.bot.wait_for("reaction_add", check=on_reaction, timeout=time)
        except asyncio.TimeoutError:
            return 2
        
        if str(reaction.emoji) == '❌': return 1
        
        if len(question["required"]) == 0: return 0

        for answer in app["answers"][app["index"]]:
            for required in question["required"]:
                if answer.Contains(required):
                    return 0
        
        await message.remove_reaction('✅', id)
        await channel.send(embed=em(
            title="Invalid Answers",
            url="https://isthicc.dev",
            description="No valid answers were detected, please answer the question and try again.",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"IsThicc Management"
        ))
        
        return self.wait_for_answers(vars, message)

    # async def sub_question(self, vars, index):
    #     pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.id not in open_apps: return
        if open_apps[message.author.id]["message_id"] != message.id: return
        # is valid message

        open_apps[message.author.id]["answers"].append(message.clean_content)
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(application_cog(bot))
