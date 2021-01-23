#
#           IsThicc-bot __main__.py | 2020 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
import asyncio
from discord.ext import commands
import os
# import datetime
from config import TOKEN
from discord_slash import SlashCommand
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
async def get_prefix(bot, message):
    """
    Get the bot's prefix.
    :param bot: Basic Discord.py "bot".
    :param message: Discord message.
    :return: Returns available prefix's.
    """
    prefixes = ["i!", "isthicc ", "thicc "]
    return commands.when_mentioned_or(*prefixes)(bot, message)
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
bot = commands.Bot(command_prefix=get_prefix, intents=discord.Intents.all())

bot.slash = SlashCommand(bot, auto_register = True, auto_delete = False)

bot.remove_command('help')
bot.load_extension('jishaku')

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
for cog_dir in os.listdir(os.getcwd()):
    if os.name == "nt":
        dir_lmao = f"{os.getcwd()}\{cog_dir}"
    else:
        dir_lmao = f"{os.getcwd()}/{cog_dir}"
    if os.path.isdir(dir_lmao) and cog_dir.startswith("cogs_"):
        for cogs in os.listdir(cog_dir):
            if cogs.endswith('.py'):
                bot.load_extension(f"{cog_dir}.{cogs[:-3]}")

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
@bot.event
async def on_ready() -> None:
    """
    Basic function to do basic tasks when the bot logs in.
    Changes status, and sends necessary messages to indicate the bot has started.

    :returns: Returns None, does the actions above
    """

    print(f'''
|--------------------|
| Bot ready!         |
| Signed in as:      |
|    {bot.user}    |
|--------------------|
    ''')

    await bot.change_presence(status=discord.Status.online,
                              activity=discord.Activity(name="Still waking up 😒, hold on!",
                                                        type=discord.ActivityType.watching))

    await asyncio.sleep(10)
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(name="IsThicc.xyz!", type=discord.ActivityType.playing))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
bot.run(TOKEN)
