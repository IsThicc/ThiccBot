#
#                             ThiccBot __main__.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import asyncio, os, aiomysql
from config   import TOKEN, mysql_db, mysql_host, mysql_password, mysql_user
from discord  import Activity, ActivityType, Status, Intents
from datetime import datetime, timezone
from db.database import Pool
from discord.ext import commands
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
    prefixes = ["I!", "i!", "isthicc ", "thicc "]
    # prefixes = ["t "]
    return commands.when_mentioned_or(*prefixes)(bot, message)

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

bot = commands.Bot(command_prefix=get_prefix, intents=Intents.all(), case_insensitive=True)
bot.slash = SlashCommand(bot)
bot.remove_command('help')
bot.load_extension('jishaku')

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def gen_timestamp(format: str = "R"):
    return f"<t:{int(datetime.now(tz=timezone.utc).timestamp())}:{format}"

setattr(bot, "gen_timestamp", gen_timestamp)
    
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

async def _init_async():
    _pool = await aiomysql.create_pool(
        host       = mysql_host,
        port       = 3306,
        db         = mysql_db,
        user       = mysql_user,
        loop       = bot.loop,
        password   = mysql_password,
        autocommit = True,
    )
    bot.db = Pool(_pool)
    await bot.db.execute_script("database.sql")

bot.loop.run_until_complete(_init_async())
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
dont_import = {"dontimportme.py"}

for cog in os.listdir("cogs"):
    if cog.endswith('.py') and cog not in dont_import:
        bot.load_extension(f"cogs.{cog[:-3]}")
        print(f"Loaded cog: cogs.{cog[:-3]}")

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
|                    |
|  Too many guilds?  |
|        {"True " if len(bot.guilds) >= 3 else "False"}       |
|--------------------|
    ''')

    await bot.change_presence(status=Status.online,
                              activity=Activity(name="Still waking up 😒, hold on!",
                                                type=ActivityType.watching))

    await asyncio.sleep(10)
    await bot.change_presence(status=Status.idle,
                              activity=Activity(name="IsThicc.dev!",
                                                type=5))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

if __name__ == '__main__':
    bot.run(TOKEN)
