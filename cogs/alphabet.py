#
#                         ThiccBot Alphebet.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, config, string
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
        self.alphabet = list(string.ascii_lowercase)
        self.delete_after = 10
        self.counting_channel = config.alphabet_channel

        self._lock = asyncio.Lock()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # TODO: Implement watching messages in the alphabet channel. This includes;
    #   - Checking the database for current letter
    #   - Determining what mode we're in. Ie. backwards, forwards, skip a letter, etc.
    #   - Do normal counting sort of checks (user, etc.)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Alphabet(bot))
