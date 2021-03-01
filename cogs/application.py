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
# time is in minutes
questions = {
    # What are you applying for?
    1 : {
        "time" : 5,
        "title" : "What are you applying for?",
        "description" : "Available positions:\n**Developer**: Help work on IsThicc's software and projects. and **Support Staff**.\n",
        "required": ["dev","developer","support","staff"]
    },
    # What coding languages do you have experience in?
    2 : {
        "time" : 5,
        "title" : "What coding languages do you have experience in?",
        "description" : "Name them separated by a comma.\nExample: `c#, python, css, ...`",
        "required": [
            "c#","c++","c","lua","js","node",
            "ada","basic","cobol","css","f#","python",
            "hackshell","html","java","javascript","js",
            "flutter","clojure","kotlin","lisp","matlab",
            "pascal","perl","php","prolog","ruby",
            "rust","sql","sqift","tcl","julia",]
    },
    # Do you have any experience in Web Development?
    3:{
        "time" : 5,
        "title" : "Do you have any experience in Web Development?",
        "description" : "This includes knowing JS, CSS and HTML.",
        "required": ["y","no","i do","don"]
    },
    # What do you like to be called? 
    4:{
        "time" : 5,
        "title" : "What do you like to be called? ",
        "description" : "Can be your username, or any nickname you prefer and are comfortable saying.",
        "required": [""]
    },
    # Who brought you to IsThicc?
    5:{
        "time" : 5,
        "title" : "What led you to applying?",
        "description" : "Did someone tell you to? If someone did, state their name, and if no one did, say why you think you applied here.",
        "required": [""]
    },
    # Rate yourself 1-10 in working with a team.
    6:{
        "time" : 5,
        "title" : "",
        "description" : "-Missing description-",
        "required": [""]
    }
    ,
    # What is your timezone?
    6:{
        "time" : 5,
        "title" : "What is your timezone?",
        "description" : "Check your current timezone [here](https://whatismytimezone.com/) and copy paste the first line ",
        "required": [""]
    }
}
'''

Rate yourself 1-10 based on experience/skill in C#
Rate yourself 1-10 based on experience/skill in C++

Explain in one paragraph why you think you should be a developer here. (Final Question.)


do you have github(if so whats your username)

'''

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
    # @commands.has_role(739510850079162530)
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
                    text="This app will auto close in 1 minute."
                ).set_thumbnail(
                    url="https://isthicc.dev/assets/img/logo.png"
                ).set_author(
                    name=member.display_name,
                    url="https://isthicc.dev",
                    icon_url=member.avatar_url
                ).add_field(
                    name="Notes", 
                    value="You will have limited time to reaspond to each question, make sure to check the footer of each embed question, there will be the time limit you'll have.",
                    inline=False
                ).add_field(
                    name="-", 
                    value="The bot will react with ✔️ when you've provided a valid answer.\nGood luck!",
                    inline=False
                ))
            await intro.add_reaction('✅')
            await intro.add_reaction('❌')

            # add to open apps
            open_apps[member.id] = {
                "message_id" : intro.id,
                "channel_id" : channel.id,
                "answers" : {},
                "index" : 0,
                "can_proceed" : False
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
            await intro.clear_reactions()
            
            # loop though questions and get answers
            for _ in range(len(questions)):
                open_apps[member.id]["index"] += 1
                open_apps[member.id]["can_proceed"] = False
                # create a list for answers
                open_apps[member.id]["answers"][open_apps[member.id]["index"]] = []
                # wait for the question to end
                code = await self.ask_question((ctx, member, channel))

                # code -> 0 = next question, 1 = quit, 2 = timeout
                if code == 1:
                    await intro.clear_reactions()
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
                    await intro.clear_reactions()
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
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))   
            await channel.send(embed=em(
                description=f"Just making sure:```py\n{open_apps[member.id]}```",
                colour=discord.Colour.gold(),
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

    async def ask_question(self, vars):
        # setup
        ctx, member, channel = vars
        app = open_apps[member.id]
        index = app["index"]
        question = questions[index]
        time = question["time"]

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
            icon_url=member.avatar_url
        ))
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        
        open_apps[member.id]["message_id"] = msg.id

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
            reaction, user = await self.bot.wait_for("reaction_add", check=on_reaction, timeout=time*60)
        except asyncio.TimeoutError:
            return 2
        
        if str(reaction.emoji) == '❌':
            return 1
        
        # if reacted with ✅
        if len(question["required"]) == 0:
            await message.clear_reactions()
            return 0

        if app["can_proceed"]:
            await message.clear_reactions()
            return 0
        
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
        
        return await self.wait_for_answers(vars, message)

    # async def sub_question(self, vars, index):
    #     pass

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.author.id not in open_apps: return
        if open_apps[message.author.id]["channel_id"] != message.channel.id: return
        i = open_apps[message.author.id]["index"]
        if i == 0: return
        open_apps[message.author.id]["answers"][i].append(message.clean_content)

        if open_apps[message.author.id]["can_proceed"]: return
        for required in questions[i]["required"]:
            if required in message.clean_content.lower():
                open_apps[message.author.id]["can_proceed"] = True
                await message.add_reaction('✔️')
                return
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(application_cog(bot))
