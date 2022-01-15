#
#                         ThiccBot Alphebet.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, config, string, enum
from discord import Embed as em
from datetime import datetime as d
from discord.ext import commands

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
"""
# For future development 
class Modes(enum.Enum):
    A_Z = ""
    Z_A = ""
    SKIP_TWO = ""
"""


# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Alphabet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.alphabet = list(string.ascii_lowercase)
        self.delete_after = 10
        self.alphabet_channel = config.alphabet_channel

        self._lock = asyncio.Lock()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def report_incorrect(self, message: discord.Message):
        await self.bad_react(message)
        await message.channel.send(embed=em(
            title="Wrong number!",
            description="You sent the wrong letter! Please try again.",
            timestamp=d.utcnow(),
            colour=discord.Colour.red()
        ).set_footer(
            text="IsThicc Alphabet",
            icon_url=self.bot.user.avatar_url
        ), delete_after=self.delete_after)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def report_user(self, message: discord.Message):
        await self.bad_react(message)
        await message.channel.send(embed=em(
            title="Oh no!",
            description="You sent the most recent letter! Please wait for someone else.",
            timestamp=d.utcnow(),
            colour=discord.Colour.red()
        ).set_footer(
            text="IsThicc Alphabet",
            icon_url=self.bot.user.avatar_url
        ), delete_after=self.delete_after)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def good_react(self, message: discord.Message):
        await message.add_reaction("✅")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def bad_react(self, message: discord.Message):
        await message.add_reaction("❌")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    async def alphabet(self, ctx: discord.Context):
        async with self._lock:
            embed = discord.Embed(colour=discord.Colour.green())
            result = await self.bot.db.execute_one(
                "SELECT Letter FROM Alphabet WHERE ChannelID = {CHANNEL};".format(
                    CHANNEL=self.alphabet_channel
                )
            )

            if result is None:
                embed.description = "You haven't setup counting in this channel yet!"
            else:
                embed.description = f"You are currently at **{self.alphabet.index(result[0])}**"

            await ctx.send(embed=embed)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # TODO: Determining what mode we're in. Ie. backwards, forwards, skip a letter, etc.

    @commands.Cog.listener(name="on_message")
    async def on_message(self, message: discord.Message):

        if message.channel.id != self.alphabet_channel:
            return

        if message.author.bot:
            return

        content = message.content.strip().lower()
        if len(content) != 1:
            return

        if content not in self.alphabet:
            return

        pos = self.alphabet.index(content)

        async with self._lock:
            try:
                result = await self.bot.db.execute_one(
                    "SELECT Letter, LastUser FROM Alphabet WHERE ChannelID = {CHANNEL};".format(
                        CHANNEL=self.alphabet_channel
                    )
                )
                if result is None:
                    raise Exception()

            except Exception as exc:
                await self.bot.db.execute(
                    "INSERT INTO Alphabet (Letter, LastUser, ChannelID) VALUES ('{LETTER}', {USER}, {CHANNEL})"
                        .format(LETTER=self.alphabet[pos], USER=message.author.id, CHANNEL=self.alphabet_channel)
                )
                return await self.good_react(message)

            if result[1] == message.author.id:
                await self.report_user(message)
                try:
                    await message.delete()
                except Exception:
                    pass
                return

            next_letter = (self.alphabet.index(result[0]) + 1)
            next_letter = next_letter if next_letter <= (len(self.alphabet) - 1) else 0

            if next_letter != pos:
                return await self.report_incorrect(message)

            await self.bot.db.execute(
                "UPDATE Alphabet SET Letter = '{LETTER}', LastUser = {USER} WHERE ChannelID = {CHANNEL}"
                    .format(LETTER=self.alphabet[next_letter], USER=message.author.id, CHANNEL=self.alphabet_channel)
            )
            await self.good_react(message)


#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Alphabet(bot))
