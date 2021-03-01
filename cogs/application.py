#
#                          IsThicc-bot Application.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, traceback, re
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
# embed_field:
# if starts with '-'  ->  Will be added into the embed as a field
# if not then into the description
# if "" -> Won't be added to embed
questions = {
    # What are you applying for?
    1 : {
        "time" : 5,
        "title" : "What are you applying for?",
        "description" : "Available positions.\n⬦ **Developer**: Help work on IsThicc's software and projects.\n⬦ **Support Staff**: -Missing description-.\n",
        "required": ["dev","developer","support","staff"],
        "embed_field" : "-Position"
    },
    # What coding languages do you have experience in?
    2 : {
        "time" : 5,
        "title" : "What coding languages do you have experience in?",
        "description" : "Name them separated by a comma.\nExample: `c#, python, css, ...`",
        "required": [],
        "embed_field" : ""
        # "required": [
        #     "c#","c++","c","lua","js","node",
        #     "ada","basic","cobol","css","f#","python",
        #     "hackshell","html","java","javascript","js",
        #     "flutter","clojure","kotlin","lisp","matlab",
        #     "pascal","perl","php","prolog","ruby",
        #     "rust","sql","sqift","tcl","julia",]
    },
    # Do you have any experience in Web Development?
    3:{
        "time" : 5,
        "title" : "Do you have any experience in Web Development?",
        "description" : "-Missing description-",
        # "description" : "This includes knowing JS, CSS and HTML.",
        "required": [],
        "embed_field" : "-Web dev experience?"
    },
    # What do you like to be called? 
    4:{
        "time" : 5,
        "title" : "What do you like to be called? ",
        "description" : "Can be your username, or any nickname you prefer and are comfortable saying.",
        "required": [],
        "embed_field" : "-Nick/Name"
    },
    # Who brought you to IsThicc?
    5:{
        "time" : 5,
        "title" : "What led you to applying?",
        "description" : "Did someone tell you to? If someone did, state their name, and if no one did, say why you think you applied here.",
        "required": [],
        "embed_field" : "What led you to applying?"
    },
    # Rate yourself 1-10 in working with a team.
    6:{
        "time" : 5,
        "title" : "Rate yourself 1-10 in working with a team.",
        "description" : "-Missing description-",
        "required": ['0','1','2','3','4','5','6','7','8','9'],
        "embed_field" : "-Working team rating"
    },
    # What is your timezone?
    7:{
        "time" : 5,
        "title" : "What is your timezone?",
        "description" : "-Missing description-",
        "required": [],
        "embed_field" : "-Timezone"
    }
}
'''
missing:
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
            channel = await ctx.guild.create_text_channel(f"app-{member.display_name}",category=category)
            await channel.set_permissions(member, send_messages=True, read_messages=True)
            await channel.set_permissions(ctx.guild.get_member(348547981253017610), send_messages=True, read_messages=True)
            
            # set some shortcut variables
            close_em=em(
                title="Closing Application",
                url="https://isthicc.dev",
                description=f"You've decided to close this application, will close in 3 seconds..\nThanks for your interest in IsThicc and goodbye!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                )
            timeout_em=em(
                title="Closing Application",
                url="https://isthicc.dev",
                description=f"Your time expired, this app will close in 3 seconds.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                )
            intro = await channel.send(embed=em(
                    title="Thicc -Developer / Staff Support- Appliaction",
                    url="https://isthicc.dev",
                    description=f"Hello {member.mention}, welcome to your app!\nWhen you're ready, react with ✅ to start or ❌ to cancel.",
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
                    value="The bot will react with 📌 when you've provided a valid answer.\nGood luck!",
                    inline=False
                ))
            await intro.add_reaction('✅')
            await intro.add_reaction('❌')

            # add the member to the open_apps
            open_apps[member.id] = {
                "message_id" : intro.id,
                "channel_id" : channel.id,
                "answers" : {},
                "index" : 0,
                "can_proceed" : False
            }

            # wait for confirmation to start the application
            try:
                def on_reaction(reaction, user):
                    # if payload.member.id not in open_apps: return False
                    return (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌") and not user.bot and open_apps[user.id] and open_apps[user.id]["message_id"] == reaction.message.id
                reaction, user = await self.bot.wait_for("reaction_add", check=on_reaction, timeout=60)
            except asyncio.TimeoutError:
                if len(open_apps[member.id]["answers"])>0:
                    return

                del open_apps[member.id]
                await channel.send(embed=timeout_em)
                await asyncio.sleep(3)
                return await channel.delete()
            
            # if the user declined, delete the channel
            if str(reaction.emoji) == '❌':
                del open_apps[member.id]
                await channel.send(embed=close_em)
                await asyncio.sleep(3)
                return await channel.delete()

            # if accepted then proceed with the questions
            await intro.clear_reactions()
            
            # loop though questions and get answers
            for _ in range(len(questions)):
                i = open_apps[member.id]["index"]+1
                open_apps[member.id]["index"] = i
                open_apps[member.id]["can_proceed"] = False
                # create a list for answers
                open_apps[member.id]["answers"][i] = []
                # wait for the question to end
                code = await self.ask_question(member.id, channel, questions[i])

                # code -> 0 = next question, 1 = quit, 2 = timeout
                if code == 1: await channel.send(embed=close_em)
                elif code == 2: await channel.send(embed=timeout_em)
                if code == 1 or code == 2:
                    del open_apps[member.id]
                    await asyncio.sleep(3)
                    return await channel.delete()

            # when all the questions are answered #

            # wait for the member to rate their languages
            langs = open_apps[member.id]["answers"][2][0].split(',')
            for language in langs:

                # uppercase the first found letter
                letter = re.search(r'\w',language)
                if letter: language = language.replace(letter[0], letter[0].upper())

                i = open_apps[member.id]["index"]+1
                open_apps[member.id]["index"] = i
                open_apps[member.id]["can_proceed"] = False
                open_apps[member.id]["answers"][i] = []
                question = {
                    "time" : 5,
                    "title":"Skill rating",
                    "description":f"Rate yourself 1-10 based on your experience/skill in **{language}**",
                }
                
                code = await self.ask_question(member.id, channel, question)
                # code -> 0 = next question, 1 = quit, 2 = timeout
                if code == 1: await channel.send(embed=close_em)
                elif code == 2: await channel.send(embed=timeout_em)
                if code == 1 or code == 2:
                    del open_apps[member.id]
                    await asyncio.sleep(3)
                    return await channel.delete()
            
            # final question
            open_apps[member.id]["index"] = 999
            open_apps[member.id]["can_proceed"] = False
            open_apps[member.id]["answers"][999] = []
            question = {
                "time" : 15,
                "title":"Final question",
                "description":"Explain in one paragraph why you think you should be accepted at IsThicc.",
            }
            code = await self.ask_question(member.id, channel, question, False)
            # code -> 0 = next question, 1 = quit, 2 = timeout
            if code == 1: await channel.send(embed=close_em)
            elif code == 2: await channel.send(embed=timeout_em)
            if code == 1 or code == 2:
                del open_apps[member.id]
                await asyncio.sleep(3)
                return await channel.delete()

            # finished taking the application!
            await channel.send(embed=em(
                title="Thank You!",
                url="https://isthicc.dev",
                description="Your app is being reviewed, we'll get back to you as soon as we can!\n- Thanks for being interested in IsThicc Software.",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ).set_thumbnail(url='https://rebin.ch/wp-content/uploads/2015/09/icon-2.png'))   

            await self.write_aplication(ctx, member, category)

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

    async def write_aplication(self, ctx, member, category):
        channel = await ctx.guild.create_text_channel(f"app-result-{member.display_name}",category=category)
        await channel.set_permissions(ctx.guild.get_member(348547981253017610), send_messages=True, read_messages=True)
        
        desc = ""
        app_em = em(
            title= f"{discord.Member} - Application" ,
            url="https://isthicc.dev",
            description=desc,
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"IsThicc Management")

        # add errythin to da embed
        for index in range(1,len(questions)+1):
            field = questions[index]["embed_field"]
            answer = open_apps[member.id]["answers"][index]
            if field == '': continue
            elif field[0] == '-':
                app_em.add_field(
                    name=field, 
                    value=answer,
                    inline=True
                )
            else:
                desc += f"⬦ **{field}**\n"
                desc += answer+'\n'
                app_em = em(
                    title= f"{member.discriminator} - Application" ,
                    url="https://isthicc.dev",
                    description=desc,
                    colour=discord.Colour.gold(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text=f"IsThicc Management")

        # add the languages and their ratings
        answers = open_apps[member.id]["answers"]
        languages = answers[2][0].split(',')
        ratings = []
        for i in range(len(answers[2])):
            ratings.append(answers[len(questions)+i+1])

        lang_value = ""

        for (i,language) in enumerate(languages):
            letter = re.search(r'\w',language)
            if letter: language = language.replace(letter[0], letter[0].upper())
            lang_value += f"{language} {ratings[i]}/10\n"
        
        app_em.add_field(
            name="Languages", 
            value=lang_value,
            inline=True
        )

        await channel.send(embed=app_em)
        del open_apps[member.id]

    async def ask_question(self, id, channel, question, change_title=True):
        # setup
        app = open_apps[id]
        index = app["index"]
        time = question["time"]
        title = f"{index}. " + question["title"]

        # send message
        msg = await channel.send(embed=em(
            title = (title if change_title else question["title"]),
            url="https://isthicc.dev",
            description=question["description"],
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"You have {time} minute(s) to answer"
        ))
        await msg.add_reaction('✅')
        await msg.add_reaction('❌')
        
        open_apps[id]["message_id"] = msg.id

        # await for reaction
        # messages are automatically collected
        # wait_for_answers() returns a 0-3 code
        return await self.wait_for_answers((time, id, channel), msg)
    
    async def wait_for_answers(self, vars, message):
        time, id, channel = vars
        app = open_apps[id]

        try:
            def on_reaction(reaction, user):
                return (str(reaction.emoji) == "✅" or str(reaction.emoji) == "❌") and not user.bot and app["message_id"] == reaction.message.id
            reaction, user = await self.bot.wait_for("reaction_add", check=on_reaction, timeout=time*60)
        except asyncio.TimeoutError:
            return 2
        
        if str(reaction.emoji) == '❌':
            return 1
        # else: reacted with ✅

        if app["can_proceed"]:
            await message.clear_reactions()
            return 0
            
        await channel.send(embed=em(
            title="Invalid Answer",
            url="https://isthicc.dev",
            description="No valid answers were detected, please answer the question and try again.",
            colour=discord.Colour.red(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"IsThicc Management"
        ))
        
        return await self.wait_for_answers(vars, message)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.author.id not in open_apps: return
        if open_apps[message.author.id]["channel_id"] != message.channel.id: return

        index = open_apps[message.author.id]["index"]
        if index == 0: return

        # if is in final question
        if index == 999:
            if not open_apps[message.author.id]["can_proceed"]:
                await message.add_reaction('📌')
            open_apps[message.author.id]["can_proceed"] = True
            open_apps[message.author.id]["answers"][index].append(message.clean_content)
            return
        
        # if is in language rating
        if index > len(questions):
            for num in ['0','1','2','3','4','5','6','7','8','9']:
                if num in message.clean_content.lower():
                    if not open_apps[message.author.id]["can_proceed"]:
                        await message.add_reaction('📌')
                    open_apps[message.author.id]["can_proceed"] = True
                    open_apps[message.author.id]["answers"][index].append(message.clean_content)
                    return
            return

        # if is in a normal question
        open_apps[message.author.id]["answers"][index].append(message.clean_content)

        if open_apps[message.author.id]["can_proceed"]: return

        req = questions[index]["required"]
        if len(req) == 0: 
            open_apps[message.author.id]["can_proceed"] = True
            await message.add_reaction('📌')
            return
        for required in questions[index]["required"]:
            if required in message.clean_content.lower():
                open_apps[message.author.id]["can_proceed"] = True
                await message.add_reaction('📌')
                return
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(application_cog(bot))
