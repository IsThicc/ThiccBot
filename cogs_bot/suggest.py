import asyncio

import discord
from discord import Embed
from discord.ext import commands


class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id != 801929449124790353 or message.author.bot: return
        content = ""
        # Remove Markdown
        msg = message.content
        for letter in msg:
            if letter == "`":
                continue
            elif letter in ['~', '_', "*", "|"]:
                if msg[msg.index(letter) + 1] == letter: # check if **, __, or ~~
                    continue
            else:
                content += letter
        ##########################

        em = Embed(title=f'New suggestion from {message.author}', colour=discord.Colour.blue(), description=content)
        msg = await self.bot.get_channel(801929480875802624).send(embed=em)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        await message.reply(f'{msg.jump_url}', delete_after=3)
        await asyncio.sleep(3)
        await message.delete()


def setup(bot):
    bot.add_cog(Suggestions(bot))