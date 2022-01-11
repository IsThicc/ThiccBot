#
#                         ThiccBot Logging.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, config
from datetime import datetime
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Logging(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Deleted Message Logger
    @commands.Cog.listener(name="on_message_delete")
    async def on_message_delete(self, message):
        if message.guild.id not in {857789766312394752, 739510335949635736} or message.embeds:
            return
        
        channel = self.bot.get_channel(config.logs_channel_id)
        embed   = discord.Embed(title=f"Deleted Message | {message.guild.name}",
                                timestamp=datetime.utcnow(),
                                colour=discord.Colour.teal())
        embed.add_field(name="Message Contents: ",
                        value=f"```{message.content}```",
                        inline=False)
        embed.add_field(name="Message Info: ",
                        value=f"Author: {message.author}\nChannel: {message.channel.name}",
                        inline=False)
        
        if message.attachments:  # if len(message.attachments) > 0:
            embed.set_image(url=message.attachments[0].url)
            
        if len(message.attachments) >= 1:
            desc = [f"[Attachment #{att + 1}]({message.attachments[att].url})" for att in range(len(message.attachments))]
            embed.add_field(name="Attachments", value=", ".join(desc), inline=False)
            
        await channel.send(embed=embed)

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    # Edited Message Logger
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.content == after.content or before.embeds:
            return

        if after.guild.id not in {857789766312394752, 739510335949635736}:
            return
        
        channel = self.bot.get_channel(config.logs_channel_id)

        if before.channel.id in {841342763102765106}:  # Ignored channels, only #tickets included
            return

        embed = discord.Embed(title=f"Edited Message | {after.guild.name}",
                              timestamp=datetime.utcnow(),
                              colour=0x8D5FF8)
        embed.add_field(name="Message Contents: ",
                        value=f"Before: ```{before.content}```\n After: ```{after.content}```",
                        inline=False)
        embed.add_field(name="Message Info: ",
                        value=f"Author: {after.author}\nChannel: {after.channel.name}\nLink: {after.jump_url}",
                        inline=False)
        
        await channel.send(embed=embed)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Logging(bot))
