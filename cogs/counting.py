#
#                         ThiccBot Counting.py | 2020-2022 (c) Mrmagicpie
#
#          Disclaimer: The sole copyright of the code belongs to Mrmagicpie. It has
#                      been written for use in another project, and is being granted
#                      use in this project. It is not subject to the general copyright
#                      claims of the code in this repository.
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, config
from discord  import Embed as em
from datetime import datetime as d
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Counting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.delete_after = 10
        self.counting_channel = config.counting_channel

        self._lock = asyncio.Lock()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def report_incorrect(self, message: discord.Message):
        await self.bad_react(message)
        await message.channel.send(embed=em(
            title="Wrong number!",
            description="You sent the wrong number! Please try again.",
            timestamp=d.utcnow(),
            colour=discord.Colour.red()
        ).set_footer(
            text="IsThicc Counting",
            icon_url=self.bot.user.avatar_url
        ), delete_after=self.delete_after)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def report_user(self, message: discord.Message):
        await self.bad_react(message)
        await message.channel.send(embed=em(
            title="Oh no!",
            description="You sent the most recent count! Please wait for someone else.",
            timestamp=d.utcnow(),
            colour=discord.Colour.red()
        ).set_footer(
            text="IsThicc Counting",
            icon_url=self.bot.user.avatar_url
        ), delete_after=self.delete_after)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def good_react(self, message: discord.Message):
        await message.add_reaction("✅")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def bad_react(self, message: discord.Message):
        await message.add_reaction("❌")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):

        if message.author.bot:
            return

        if message.channel.id != self.counting_channel:
            return

        if not message.content.isdigit():
            return

        async with self._lock:
            count  = int(message.content)

            if count <= 0:
                return await self.report_incorrect(message)

            try:
                result  = await self.bot.db.execute_one(
                    "SELECT Count, LastUser FROM Counting WHERE ChannelID = {CHANNEL};".format(
                        CHANNEL=self.counting_channel
                    )
                )
                if result is None:
                    raise Exception()

            except Exception as exc:
                # print(exc)
                await self.bot.db.execute(
                    "INSERT INTO Counting (Count, LastUser, ChannelID) VALUES ({COUNT}, {USER}, {CHANNEL})"
                        .format(COUNT=count, USER=message.author.id, CHANNEL=self.counting_channel)
                )
                return await self.good_react(message)

            if result[1] == message.author.id:
                await self.report_user(message)
                try:
                    await message.delete()
                except Exception:
                    pass
                return

            next_count = (result[0] + 1)

            if next_count != count:
                return await self.report_incorrect(message)

            await self.bot.db.execute(
                "UPDATE Counting SET Count = {COUNT}, LastUser = {USER} WHERE ChannelID = {CHANNEL}"
                    .format(COUNT=count, USER=message.author.id, CHANNEL=self.counting_channel)
            )
            await self.good_react(message)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Counting(bot))
