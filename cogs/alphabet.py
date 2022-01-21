#
#                         ThiccBot Alphebet.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, config, string, random
from discord  import Embed as em
from datetime import datetime as d
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Alphabet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._lock = asyncio.Lock()
        self.alphabet = list(string.ascii_lowercase)
        self.alphabet_len = len(self.alphabet)
        self.delete_after = 10
        self.alphabet_channel = config.alphabet_channel

        self.wrong_emoji = "❌"
        self.right_emoji = "✅"

        self.MODES = {
            "A_Z": self._az_check,
            "Z_A": self._za_check,
            "SKIP_TWO": self._skiptwo_check
        }
        self.MODE_DESCRIPTIONS = {
            "A_Z": "The **A-Z** mode the classic alphabet mode, "
                   "say every letter between A and Z in order.",
            "Z_A": "The **Z-A** mode the reverse of the classic alphabet mode, "
                   "say every letter between Z and A in reverse order.",
            "SKIP_TWO": "The **Skip Two** mode is what the name says, "
                        "say every __other__ letter between A and Z."
        }
        self.MODE_FIRST_LETTER = {
            "A_Z": "a",
            "Z_A": "z",
            "SKIP_TWO": "a"
        }

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _az_check(self, message, content, sql_result):
        if not (await self._check_user(message, sql_result[1])):
            return

        pos = self.alphabet.index(content)
        next_letter = (self.alphabet.index(sql_result[0]) + 1)
        next_letter = (next_letter if next_letter <= (self.alphabet_len - 1) else 0)

        if next_letter == 0 and content == "z":
            new_mode = await self._get_new_mode("A_Z")
            await self.bot.db.execute(
                "UPDATE Alphabet SET Letter = '{LETTER}', LastUser = {USER} WHERE ChannelID = {CHANNEL}, MODE = '{MODE}'"
                    .format(
                        LETTER=self.MODE_FIRST_LETTER.get(new_mode, "a"),
                        # LETTER=self.alphabet[next_letter],
                        USER=message.author.id,
                        CHANNEL=self.alphabet_channel, MODE=new_mode
                    )
            )
            return await message.channel.send(embed=self.bot.ef(em(
                title="Alphabet switch up!",
                description="The alphabet mode has switched! Here is the description for this mode:\n\n"
                            f"{self.MODE_DESCRIPTIONS[new_mode]}",
                colour=discord.Colour.teal()
            ), "Alphabet"))

        if next_letter != pos:
            return await self.report_incorrect(message)

        await self.bot.db.execute(
            "UPDATE Alphabet SET Letter = '{LETTER}', LastUser = {USER} WHERE ChannelID = {CHANNEL}"
                .format(LETTER=self.alphabet[next_letter], USER=message.author.id, CHANNEL=self.alphabet_channel)
        )
        await message.add_reaction(self.right_emoji)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _za_check(self, message, content, sql_result):
        if not (await self._check_user(message, sql_result[1])):
            return

        pos = self.alphabet.index(content)
        next_letter = (self.alphabet.index(sql_result[0]) - 1)
        next_letter = (next_letter if next_letter <= (self.alphabet_len - 1) else 0)  # TODO: Test this logic

        if next_letter == 0 and content == "a":
            new_mode = await self._get_new_mode("Z_A")
            await self.bot.db.execute(
                "UPDATE Alphabet SET Letter = '{LETTER}', LastUser = {USER} WHERE ChannelID = {CHANNEL}, MODE = '{MODE}'"
                    .format(
                    LETTER=self.MODE_FIRST_LETTER.get(new_mode, "a"),
                    USER=message.author.id,
                    CHANNEL=self.alphabet_channel, MODE=new_mode
                )
            )
            return await message.channel.send(embed=self.bot.ef(em(
                title="Alphabet switch up!",
                description="The alphabet mode has switched! Here is the description for this mode:\n\n"
                            f"{self.MODE_DESCRIPTIONS[new_mode]}",
                colour=discord.Colour.teal()
            ), "Alphabet"))

        if next_letter != pos:
            return await self.report_incorrect(message)

        await self.bot.db.execute(
            "UPDATE Alphabet SET Letter = '{LETTER}', LastUser = {USER} WHERE ChannelID = {CHANNEL}"
                .format(LETTER=self.alphabet[next_letter], USER=message.author.id, CHANNEL=self.alphabet_channel)
        )
        await message.add_reaction(self.right_emoji)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _skiptwo_check(self, message, content, sql_result):

        # I don't want to do this rn lmao
        new_mode = await self._get_new_mode("Z_A")
        await self.bot.db.execute(
            "UPDATE Alphabet SET Letter = '{LETTER}', LastUser = {USER} WHERE ChannelID = {CHANNEL}, MODE = '{MODE}'"
                .format(
                LETTER=self.MODE_FIRST_LETTER.get(new_mode, "a"),
                USER=message.author.id,
                CHANNEL=self.alphabet_channel, MODE=new_mode
            )
        )
        return await message.channel.send(embed=self.bot.ef(em(
            title="Alphabet switch up!",
            description="The alphabet mode has switched! Here is the description for this mode:\n\n"
                        f"{self.MODE_DESCRIPTIONS[new_mode]}",
            colour=discord.Colour.teal()
        ), "Alphabet"))

        # if not (await self._check_user(message, sql_result[1])):
        #     return
        #
        # pos = self.alphabet.index(content)
        # next_letter = (self.alphabet.index(sql_result[0]) + 2)
        #
        # if next_letter > self.alphabet_len:
        #     ...
        # # next_letter = (next_letter if next_letter <= (len(self.alphabet) - 1) else 0)
        # # FIXME: The logic hasn't even been thought about xd

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _mode_not_found(self, message, content, sql_result):
        await message.channel.send(embed=self.bot.ef(em(
            title="Oh no, an error occurred!",
            description="An error occurred while trying to find the correct Alphabet mode! "
                        "This error can only be fixed by a member of management! Please alert them if it continues.",
            colour=discord.Colour.red()
        ), "Alphabet"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    async def alphabet(self, ctx: commands.Context):
        async with self._lock:
            result = await self.bot.db.execute_one(
                "SELECT Letter FROM Alphabet WHERE ChannelID = {CHANNEL};".format(CHANNEL=self.alphabet_channel)
            )

            await ctx.send(embed=self.bot.ef(em(
                colour=discord.Colour.green(),
                description=("You haven't setup alphabet in this channel yet!"
                                if (result is None) else
                             f"Alphabet is currently at **{result[0]}**")
            ), "Alphabet"))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

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

        async with self._lock:
            try:
                result  = await self.bot.db.execute_one(
                    "SELECT Letter, LastUser, Mode FROM Alphabet WHERE ChannelID = {CHANNEL};".format(
                        CHANNEL=self.alphabet_channel
                    )
                )
                if result is None:
                    raise Exception()

            except Exception as exc:
                # This should only happen the first time that the bot has a table without the current channels id
                await self.bot.db.execute(
                    "INSERT INTO Alphabet (Letter, LastUser, ChannelID, Mode) VALUES ('{LETTER}', {USER}, {CHANNEL}, '{MODE}')"
                        .format(LETTER=self.alphabet[self.alphabet.index(content)],
                                USER=message.author.id, CHANNEL=self.alphabet_channel, MODE="A_Z")
                )
                return await message.add_reaction(self.right_emoji)

            coroutine = self.MODES.get(result[2], self._mode_not_found)
            return await coroutine(message, content, result)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _get_new_mode(self, prev_mode: str):
        modes = list(self.MODES.keys())
        modes.remove(prev_mode)
        return random.choice(modes)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def _check_user(self, message: discord.Message, id: int):
        if id == message.author.id:
            await self.report_user(message)
            try:
                await message.delete()
                return False
            except discord.errors.DiscordException:
                return False
        return True

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def report_incorrect(self, message: discord.Message):
        await message.add_reaction(self.wrong_emoji)
        return await message.channel.send(embed=self.bot.ef(em(
            title="Wrong number!",
            description="You sent the wrong letter! Please try again.",
            timestamp=d.utcnow(),
            colour=discord.Colour.red()
        ), "Alphabet"), delete_after=self.delete_after)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def report_user(self, message: discord.Message):
        await message.add_reaction(self.wrong_emoji)
        return await message.channel.send(embed=self.bot.ef(em(
            title="Oh no!",
            description="You sent the most recent letter! Please wait for someone else.",
            timestamp=d.utcnow(),
            colour=discord.Colour.red()
        ), "Alphabet"), delete_after=self.delete_after)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Alphabet(bot))
