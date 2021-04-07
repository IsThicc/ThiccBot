#
#                          IsThicc-bot Project.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, traceback, re, json, requests
from discord.ext          import commands
from discord.ext.commands import BucketType
from discord              import Embed as em
from datetime             import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
open_projects = {}
service_format = {
    1 : {
        "title" : "Service Name",
        "description" : "Type in the name of the service to create.",
    },
    2 : {
        "title" : "URL",
        "description" : "Um.. idk",
    },
    3 : {
        "title" : "VPS",
        "description" : "Lol hi",
    },
    4 : {
        "title" : "Sudo",
        "description" : "Poggers",
    }
}
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Project(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="project", aliases=["proj"])
    @commands.cooldown(1, 1, BucketType.user)
    @commands.has_role(739510850079162530)
    async def project(self, ctx, member, option=None, extra: str = None):
        try:
            app_uri = f'http://10.42.10.4:5000/staff/project/{member.name}'
            
            if option == "create":
                data = {
                    "contact" : {
                        "email" : "none",
                        "webhook" : None
                    },
                    "services" : { },
                }
                data = json.dumps(data, separators=(',',':'))

                headers = {
                    "project": data
                }
                x = requests.post(app_uri, headers=headers)
                data = x.json()
                file = data["file"]

                if self.parse_error(ctx, data): return
                return await ctx.send(embed=em(
                    title=f"Project Create",
                    description="Successfully edited the contact e-mail address of {member.name}.\nFile: {file}",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                ))
            
            elif option == "contact":
                if extra == None:
                    return await ctx.send(embed=em(
                        title="Yikes! You forgot to supply a contact email!",
                        colour=discord.Colour.red(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Management"
                    ))
                
                matches = re.search(".+@.+\.\w\w\w", extra)
                if not matches:
                    return await ctx.send(embed=em(
                        title="The email you suppied isn't valid!",
                        colour=discord.Colour.red(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Management"
                    ))

                data = {
                    "contact" : {
                        "email" : "owner@isthicc.xyz",
                        "webhook" : None
                    },
                }
                data    = json.dumps(data, separators=(',', ':'))
                headers = {"edit": data}
                x       = requests.post(app_uri, headers=headers)
                data    = x.json()
                file    = data["file"]
                
                if self.parse_error(ctx, data): return

                return await ctx.send(embed=em(
                    title=f"Project Edit",
                    description="Successfully edited the contact e-mail address of {member.name}.\nFile: {file}",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Management"
                ))
            
            elif option == "service":
                if extra == None:
                    return await ctx.send(embed=em(
                        title="Yikes! You forgot to supply a contact email!",
                        colour=discord.Colour.red(),
                        timestamp=datetime.utcnow()
                    ).set_footer(
                        icon_url=self.bot.user.avatar_url,
                        text="IsThicc Management"
                    ))

                # start setup
                await self.service(ctx, ctx.member)


        except Exception as e:
            print(traceback.format_exc())
            return await ctx.send(content="<@348547981253017610>", embed=em(
                title="Uh oh, there's an error!",
                description=f"```py\n{traceback.format_exc()}```",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Staff"
            ))


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def parse_error(self, ctx, data):
        if data["error"]:
            await ctx.send(embed=em(
                title="Error",
                description=data["error"],
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            ).set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Management"
            ))
            return True
        return False


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # setup service
    async def service(self, ctx, member):
        id = member.id
        if id in open_projects: del open_projects[id]

        # create channel and send message
        category = discord.utils.get(ctx.guild.categories, name='『 Staff Development 』')
        channel  = await ctx.guild.create_text_channel(f"app-{member.display_name}",category=category)
        await channel.set_permissions(member, send_messages=True, read_messages=True)
        # await channel.set_permissions(ctx.guild.get_member(348547981253017610), send_messages=True, read_messages=True)
            
        # set some shortcut variables
        close_em = em(
                url="https://isthicc.dev",
                title=f"Setup canceled",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
                ).set_footer(
                    icon_url=self.bot.user.avatar_url,
                    text="IsThicc Management"
                )
           
        # add the member to the open_projects
        open_projects[id] = {
                "channel_id" : channel.id,
                "answers" : {},
                "index" : 0,
        }

        # loop though the service format and get answers
        for _ in range(len(service_format)):

            i = open_projects[id]["index"] + 1
            open_projects[id]["index"] = i

            # create a list for answers
            open_projects[id]["answers"][i] = []
            # wait for the question to end
            timed_out = await self.ask_question(id, ctx, service_format[i])

            if timed_out: return await channel.send(embed=close_em)

        await self.save_data(member, ctx)


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def ask_question(self, id, ctx, question):
        app   = open_projects[id]
        index = app["index"]
        title = f"{index}. " + question["title"]

        # send message
        await ctx.send(embed=em(
            title=question["title"],
            url="https://isthicc.dev",
            description=question["description"],
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"You have 1 minute to answer"
        ))
        
        app = open_projects[id]

        try:
            def wait_message(message):
                return not message.author.bot and message.author.id in open_projects and open_projects[message.author.id]["channel_id"] == message.channel.id
            message = await self.bot.wait_for("on_message", check=wait_message, timeout=60)
        except asyncio.TimeoutError:
            return True

        index = open_projects[message.author.id]["index"]
        open_projects[message.author.id]["answers"][index].append(message.clean_content)

        return False


    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def save_data(self, member, ctx):
        # update this to the real address
        app = open_projects[member.id]
        app_uri = f'http://10.42.10.4:5000/staff/project/{member.name}'

        # (the caps in the keys don't matter)
        title = app["answers"][0]
        data = {
            title : {
                "url":  app["answers"][1],
                "vps":  app["answers"][2],
                "sudo": app["answers"][3],
                "user": "none"
            }
        }


        await ctx.send(embed=em(
            title = "Output",
            url="https://isthicc.dev",
            description=f"```{data[title]}```",
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=self.bot.user.avatar_url,
            text=f"IsThicc Management"
        ))

        return

        data = json.dumps(data, separators=(',',':'))
        headers = {
            "add": data
        }

        x = requests.post(app_uri, headers=headers)
        data = x.json()
        file = data["file"]

        print(f"Saved as file {file}")

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Project(bot))
