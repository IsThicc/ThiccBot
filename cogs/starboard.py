#
#                          IsThicc-bot Starboard.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord
from discord.ext import commands
from typing      import Optional
from datetime    import datetime as d
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Starboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    async def __get_message(self, payload: discord.RawReactionActionEvent) -> Optional[discord.Message]:

        starboard = self.bot.get_channel(816095466067722250)
        channel   = self.bot.get_channel(payload.channel_id)
        msg       = await channel.fetch_message(payload.message_id)

        async for message in starboard.history():
            if str(msg.id) in message.content:
                return message
        
        return None

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
    
    async def __update_starboard(self, count: int, payload: discord.RawReactionActionEvent):

        channel   = self.bot.get_channel(payload.channel_id)
        starboard = self.bot.get_channel(816095466067722250)
        msg       = await channel.fetch_message(payload.message_id)

        async for message in starboard.history():
            if str(msg.id) in message.content:
                await message.edit(content=f"{'⭐' if count < 10 else '🌟'} **{count}** {channel.mention} ID: {msg.id}")
                if count > 10:
                    await message.pin(reason='Starboard message over 10 reactions.')
                break

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):

        user      = self.bot.get_user(payload.user_id)
        channel   = self.bot.get_channel(payload.channel_id)
        starboard = self.bot.get_channel(816095466067722250)
        msg       = await channel.fetch_message(payload.message_id)

        if user.bot or payload.guild_id is None: return  # so no screech

        if str(payload.emoji) != '⭐': return  # id rather not star every reacted message lmfao

        for reaction in msg.reactions:
            if str(reaction) == '⭐':
                reactions = len(await reaction.users().flatten())

                if reactions != 1:
                    return await self.__update_starboard(reactions, payload)

                embed = discord.Embed(colour=discord.Colour.gold(), description=f"{msg.content}\n[Jump!]({msg.jump_url})", timestamp=d.utcnow())
                embed.set_footer(text="IsThicc Starboard", icon_url=self.bot.user.avatar_url)

                if msg.attachments:
                        embed.set_image(url=msg.attachments[0].url)
                if len(msg.attachments) >= 1:
                    attachmenturls = [att.url for att in msg.attachments]
                    embed.add_field(name="Attachments", value="\n".join(attachmenturls))

                await starboard.send(f"⭐ **{reactions}** {channel.mention} ID: {msg.id}", embed=embed)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):

        channel = self.bot.get_channel(payload.channel_id)
        user    = self.bot.get_user(payload.user_id)

        if user.bot is None: return
        if str(payload.emoji) != '⭐': return

        msg = await channel.fetch_message(payload.message_id)

        for reaction in msg.reactions:
            if str(reaction) == '⭐':
                reactions = len(await reaction.users().flatten())

                if reactions >= 1:
                    return await self.__update_starboard(reactions, payload)

        message = await self.__get_message(payload)
        return await message.delete()

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Starboard(bot))
