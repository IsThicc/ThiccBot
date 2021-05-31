#
#                          IsThicc-bot Tickets.py | 2020-2021 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio
from discord.ext import commands
from discord     import Embed as em
from datetime    import datetime
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#

class Tickets(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db  = bot.db

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        emoji         = str(payload.emoji)
        open_channel  = self.bot.get_channel(806012160198705183)
        reaction_user = self.bot.get_user(payload.user_id)
        guild         = await self.bot.fetch_guild(payload.guild_id)
        av            = self.bot.user.avatar_url

        if payload.channel_id != open_channel.id:
            return

        msg = await open_channel.fetch_message(payload.message_id)

        if emoji != "custom ticket emoji":
            return

        opening = em(
            title=f"Opening new ticket for {reaction_user.display_name}",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        opening.set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        )

        await msg.remove_reaction(emoji, reaction_user)
        await open_channel.send(embed=opening, delete_after=5)

        priority_embed = em(
            title="Please choose a priority below!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        priority_embed.add_field(
            name="Low:",
            value=":green_circle:",
            inline=True
        )
        priority_embed.add_field(
            name="Medium:",
            value=":yellow_circle:",
            inline=True
        )
        priority_embed.add_field(
            name="High:",
            value=":red_circle:",
            inline=True
        )
        priority_embed.set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        )
        try:
            dm_msg = await reaction_user.send(embed=priority_embed, timeout=10)
            await dm_msg.add_reaction("🟢")  # Green
            await dm_msg.add_reaction("🟡")  # Yellow
            await dm_msg.add_reaction("🔴")   # Red

            def priority_check(reaction, user):
                emoji = str(reaction.emoji)
                return user.id == reaction_user.id and reaction.channel == reaction_user.dm_channel \
                       and emoji == "🟢" \
                       or emoji == "🟡" \
                       or emoji == "🔴"

            reaction, user = await self.bot.wait_for("reaction_add", check=priority_check)

            if str(reaction.emoji) == "🟢":
                priority = ["Low", "🟢"]
            elif str(reaction.emoji) == "🟡":
                priority = ["Medium", "🟡"]
            else:
                priority = ["High", "🔴"]

            topic_embed = em(
                title="What do you want your ticket to be about?",
                colour=discord.Colour.green(),
                timestamp=datetime.utcnow()
            )
            topic_embed.set_footer(
                icon_url=av,
                text="IsThicc Tickets"
            )
            dm_msg = await reaction_user.send(embed=topic_embed, timeout=60)
            await dm_msg.add_reaction("🟢")  # Green
            await dm_msg.add_reaction("🟡")  # Yellow
            await dm_msg.add_reaction("🔴")   # Red

            def topic_check(m):
                return user.id == reaction_user.id and user.id == reaction_user.dm_channel

            topic = await self.bot.wait_for("message", check=topic_check)

        except asyncio.TimeoutError:
            timeout_e = em(
                title="You ran out of time! Please try again!",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            timeout_e.set_footer(
                icon_url=av,
                text="IsThicc Tickets"
            )
            return await dm_msg.edit(embed=timeout_e)

        time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")
        category = discord.utils.get(guild.categories, name="『 Tickets 』")

        ticket = await guild.create_text_channel(
            name=f'Ticket-{reaction_user.display_name}',
            category=category,
            topic=f"Ticket opened by {reaction_user.mention} at {time}! Priority: {priority[1]}"
        )

        opened = em(
            description=f"Ticket opened for {reaction_user.mention} at {time}!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        opened.add_field(
            name="Priority",
            value=": ".join(priority),
            inline=True
        )
        opened.add_field(
            name="Topic",
            value=topic,
            inline=True
        )
        opened.set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        )
        await ticket.send(content="<@!796953153010532362>", embed=opened)

        await self.db.execute('INSERT INTO tickets VALUES(' + str(ticket.id) + ', ' + str(reaction_user.id) + ', true)')
        # parse as str in query, but the database will parse it as whatever you chose it to be in phpmyadmin.

        #   # Channel id(ticket.id):                 ticket_id
        #   # Ticket opener id(reaction_user.id):    user_id
        #   # Open or closed(bool: true):            open_close

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    async def close(self, ctx):

        av = self.bot.user.avatar_url

        try:
            r = await self.db.execute('SELECT * FROM tickets WHERE channel_id = ' + str(ctx.channel.id))
        except Exception:
            not_ticket = em(
                title="Sorry!",
                description="Sorry! This channel isn't a ticket. Please use this command again in a ticket.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            not_ticket.set_footer(
                icon_url=av,
                text="IsThicc Tickets"
            )
            return await ctx.send(embed=not_ticket)

        closing = em(
            title="Closing in 3 seconds!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        closing.set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        )

        await self.db.execute('UPDATE tickets SET closing = false WHERE channel_id = ' + str(ctx.channel.id))
        user = await self.db.execute("SELECT user_id FROM tickets WHERE channel_id = " + str(ctx.channel.id))

        msg    = await ctx.send(embed=closing)
        user   = await self.bot.get_user(user[0])
        closed = discord.utils.get(ctx.guild.categories, name="『 Archived Tickets 』")
        time   = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

        await ctx.channel.edit(
            name=f"Archived-{user.display_name}",
            topic=f"Ticket opened by {user.mention}. Closed by {ctx.author.mention} at {time}!",
            category=closed,
            reason="Ticket Closed."
        )
        await asyncio.sleep(3)

        closed = em(
            title="Ticket closed!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        )
        closed.set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        )
        await msg.edit(embed=closed)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Tickets(bot))
