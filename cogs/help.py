#
#                         IsThicc-bot Help.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
from discord.ext          import commands
from discord.ext.commands import BucketType
from discord              import Embed as em
from datetime             import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @commands.cooldown(1, 1, BucketType.user)
    async def help(self, ctx):
        """
        "Help" command. Send a nice embed to show IsThicc help.
        :param ctx: Basic Discord.py context.
        :return: Returns Help embed.
        """

        if ctx.author.permissions_in(self.bot.get_channel(744010240542113792)).send_messages:

            command_list = {}
            commands     = {}

            help = em(
                title="Staff Help!",
                description="",
                colour=discord.Colour.gold(),
                timestamp=datetime.utcnow()
            )

            # I'll probably rewrite this later without so many for's but it's fine for now.
            for command in self.bot.commands:

                if command.cog_name not in commands:
                    command_list[command.cog_name] = []

                command_list[command.cog_name].append(command.name)
                for alias in command.aliases:
                    command_list[command.cog_name].append(alias)

                if type(command) is not discord.ext.commands.Group or command.name.startswith("jishaku"): continue

                for subcommand in command.commands:
                    command_list[command.cog_name].append(f"{command.name} {subcommand.name}")

            for cog_num, cog in enumerate(command_list):
                if cog_num == 23:
                    help.add_field(
                        name="And more!",
                        value="Sorry! I couldn't show all commands because there's more than 25 bot cogs!"
                    )
                    break

                help.add_field(
                    name=f"{cog} Commands!",
                    value="``" + "`` | ``".join(command_list[cog]) + "``"
                )

            help.set_footer(
                icon_url=self.bot.user.avatar_url,
                text="IsThicc Staff"
            )

            return await ctx.send(embed=help)

        return await ctx.send(embed=em(
            title="IsThicc Help!",
            description="""
The IsThicc bot is a work-in-progress bot to help our staff with server management!

The IsThicc Bot doesn't currently have any public commands! Please check back later. If you have questions with the bot or any of questions please don't hesitate to reach out to our staff in <#744252916684161094>!
            """,
            colour=discord.Colour.gold(),
            timestamp=datetime.utcnow()
        ).set_footer(
            text="IsThicc Software",
            icon_url=self.bot.user.avatar_url
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command(name="test")
    async def test(self, ctx):
        await ctx.send("test you hoe :heart:")

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Help(bot))
