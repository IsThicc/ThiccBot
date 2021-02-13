#
#                          IsThicc-bot __main__.py | 2020 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import asyncio, os, aiomysql, discord
from config import TOKEN, mysql_db, mysql_host, mysql_password, mysql_user
from discord.ext import commands
from discord_slash import SlashCommand
from discord import Activity, ActivityType, Status, Intents
from db.database import Pool
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
bot = commands.Bot(command_prefix=get_prefix, intents=Intents.all())
bot.slash = SlashCommand(bot, auto_register=True, auto_delete=False)
bot.remove_command('help')
bot.load_extension('jishaku')
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
async def _init_async():
    _pool = await aiomysql.create_pool(
        host = mysql_host,
        port = 3306,
        db = mysql_db,
        user = mysql_user,
        password = mysql_password,
        autocommit = True,
        loop = bot.loop
    )

    bot.db = Pool(_pool)

    await bot.db.execute('CREATE TABLE IF NOT EXISTS tags(name VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL PRIMARY KEY, content VARCHAR(150) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL, owner BIGINT NOT NULL, command_id BIGINT NOT NULL, createdate DATETIME)')
    
    tickets_query = 'CREATE TABLE IF NOT EXISTS tickets(channel_id THICCINT NOT NULL PRIMARY KEY, user_id EXTREMLY_THICC_INT NOT NULL, open BOOLEAN HAS_TO_EXIST_KEK)'
    await bot.db.execute(tickets_query.replace('THICCINT', 'BIGINT').replace('EXTREMLY_THICC_INT', 'BIGINT').replace('HAS_TO_EXIST_KEK', 'NOT NULL'))
    
    await bot.db.execute('CREATE TABLE IF NOT EXISTS warnings(warn_id VARCHAR(30) CHARACTER SET utf8 COLLATE utf8_swedish_ci NOT NULL PRIMARY KEY, user_id BIGINT NOT NULL)')
    
bot.loop.run_until_complete(_init_async())

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

    await bot.change_presence(status=Status.online,
                              activity=Activity(name="Still waking up 😒, hold on!",
                                                        type=ActivityType.watching))

    await asyncio.sleep(10)
    await bot.change_presence(status=Status.dnd, activity=Activity(name="IsThicc.xyz!", type=ActivityType.playing))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
bot.run(TOKEN)
