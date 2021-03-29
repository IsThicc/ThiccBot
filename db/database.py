#
#                          IsThicc-bot Database.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import aiomysql
from datetime import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Pool:
    def __init__(self, pool):
        self.pool = pool

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # Base Methods

    async def execute(self, query: str, options: tuple = None) -> list:
        """
        :param query: Query str to execute to MySQL Database
        :param options: Options tuple for query, can be None
        :return: returns nested list/fetchall result
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, options)
                return await cursor.fetchall()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def execute_one(self, query: str, options: tuple = None) -> list:
        """
        :param query: Query str to execute to MySQL Database
        :param options: Options tuple for query, can be None
        :return: returns nested list/fetchone result
        """
        async with self.pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, options)
                return await cursor.fetchone()

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Helper Methods
    
    # Tags
    
    async def add_tag(self, tag: str, content: str, owner: int, command_id: int) -> None:
        """
        :param tag: tag name
        :param content: tag content
        :return: returns None
        """
        fmt = datetime.now().strftime('%Y-%m-%d')
        await self.execute("INSERT INTO tags VALUES('" + tag + "','" + content + "','" + str(owner) + "','" + str(command_id) + "','" + str(fmt) + "')") # it dosent like the ? eeee

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def remove_tag(self, tag: str) -> int:
        """
        :param tag: tag name to delete
        :return: returns the command id
        """
        r = await self.execute("SELECT command_id FROM tags WHERE name = '" + tag + "'")
        await self.execute("DELETE FROM tags WHERE name = '" + tag + "'")

        return r[0]

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    # Mod
    
    async def warn(self, _id: int, reason: str, datetime: datetime, current: bool, warnid: str) -> None:
        await self.execute("INSERT INTO warnings VALUES('" + str(_id) + "','" + reason + "'," + datetime + "," + current + ",)")

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    async def unwarn(self, warnid: int):
        await self.execute("UPDATE warnings SET current = false WHERE warn_id = '" + warnid + "'")

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
