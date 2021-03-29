#
#                          IsThicc-bot Suggest.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio, re
from discord     import Embed as em
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Suggestions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_message(self, message):

        if message.channel.id != 801929449124790353 or message.author.bot: return
        
        content = re.sub(r'~~|\|\||__|\*\*|`+', "", message.content)
            
        embed = em( 
            colour=discord.Colour.blue(),
            description=f"```{content}```"
        ).set_author(
            name=f"New suggestion from {message.author}",
            icon_url=message.author.avatar_url
        )
        
        if message.attachments:
            try:
               embed.set_image(url=attachment[0].url)
               if len(message.attachments) != 1:
                   embed.add_field("Attachments", "\n".join(a.url for a in message.attachments))
            except Exception as e:
                await message.channel.send(e)
 
        msg = await self.bot.get_channel(801929480875802624).send(embed=embed)

        await msg.add_reaction('👍')
        await msg.add_reaction('👎')

        await message.reply(f'{msg.jump_url}', delete_after=5, mention_author=False)
        await message.delete()

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Suggestions(bot))
