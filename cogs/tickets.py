#
#                          ThiccBot Tickets.py | 2020-2022 (c) IsThicc
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
import discord, asyncio
from enum import Enum
from discord import Embed as em
from datetime import datetime
from config import (tickets_category_id,
                    tickets_archived_category_id,
                    tickets_open_channel_id,
                    logs_channel_id)
from discord.ext import commands
#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class InsufficientTicketPermissions(commands.CheckFailure):
    pass

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

class Priority(Enum):
    """Priority Enum
    A enum to represent the ticket priority, (how it should be ranked based on how urgent it is, etc...)

    Example:
        >>> priority = Priority.HIGH
        >>> print(f"Ticket priority: {priority.value}")
        Ticket priority: High
    """
    LOW    = "Low"     # 1
    MEDIUM = "Medium"  # 2
    HIGH   = "High"    # 3

# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

def has_ticket_permissions():
    async def decorator(ctx):
        try:
            await ctx.bot.db.execute('SELECT 1 FROM tickets WHERE channel_id = ' + str(ctx.channel.id))
        except Exception:
            not_ticket = em(
                title="Sorry!",
                description="Sorry! This channel isn't a ticket. Please use this command again in a ticket.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            not_ticket.set_footer(
                icon_url=ctx.author.avatar_url,
                text="IsThicc Tickets"
            )
            return await ctx.send(embed=not_ticket)

        user = await ctx.bot.db.execute("SELECT user_id FROM tickets WHERE channel_id = " + str(ctx.channel.id))
        user = ctx.bot.get_user(user[0][0])

        if ctx.author == user or ctx.guild.get_role(796953153010532362) in ctx.author.roles:
            return True
        raise InsufficientTicketPermissions()

    return commands.check(decorator)

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
class Tickets(commands.Cog):
    def __init__(self, bot):
        self.db  = bot.db
        self.bot = bot
        self.priorities = {
            "🟢": Priority.LOW,
            "🟡": Priority.MEDIUM,
            "🔴" : Priority.HIGH
        }

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        emoji = str(payload.emoji)
        open_channel  = self.bot.get_channel(tickets_open_channel_id)
        logs_channel  = self.bot.get_channel(logs_channel_id)
        reaction_user = self.bot.get_user(payload.user_id)
        av = self.bot.user.avatar_url

        if None in {open_channel, logs_channel}:
            return

        if payload.channel_id != open_channel.id:
            return

        msg = await open_channel.fetch_message(payload.message_id)

        if emoji != "<:ticket:849650925625671707>":
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

        topic_embed = em(
            title="What is your ticket about?",
            timestamp=datetime.utcnow(),
            colour=discord.Colour.green(),
        ).set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        )

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
            inline=True,
            value=":yellow_circle:",

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

        priority_message = await reaction_user.send(embed=priority_embed)

        await priority_message.add_reaction(emoji="🟢")
        await priority_message.add_reaction(emoji="🟡")
        await priority_message.add_reaction(emoji="🔴")

        try:
            def check(r, u):
                return r.emoji in self.priorities and u == reaction_user and r.message.channel == reaction_user.dm_channel

            def topic_check(m):
                return m.author == reaction_user and m.channel == reaction_user.dm_channel

            reaction, user = await self.bot.wait_for("reaction_add", check=check, timeout=60)
            priority = self.priorities[reaction.emoji]
            await priority_message.add_reaction(emoji="✅")
            topic_message = await reaction_user.send(embed=topic_embed)

            message = await self.bot.wait_for("message", check=topic_check, timeout=60)
            await topic_message.add_reaction(emoji="✅")
            topic = message.content

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
            return await reaction_user.send(embed=timeout_e)

        guild = self.bot.get_guild(payload.guild_id)
        category = discord.utils.get(guild.categories, id=tickets_category_id)

        for attempt in [0, 1]:  # range(2):
            try:
                ticket = await guild.create_text_channel(
                    name=f'ticket-{reaction_user.display_name}',
                    category=category,
                    topic=f"Ticket opened by {reaction_user.mention}. Priority: {priority.value}"
                )
                await ticket.set_permissions(reaction_user, read_messages=True, send_messages=True)

                opened = em(
                    description=f"Ticket opened for {reaction_user.mention}!",
                    colour=discord.Colour.green(),
                    timestamp=datetime.utcnow()
                )
                opened.add_field(
                    name="Priority",
                    value=priority.value,
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
                await ticket.send(content="<@&796953153010532362>", embed=opened)
                break

            except:
                if attempt == 1:
                    return await logs_channel.send(content="<@&796953153010532362>", embed=discord.Embed(
                        title="Failed to create ticket!",
                        description=f"Failed to create ticket channel for {reaction_user.mention}. Does the bot have the correct permissions?",
                        colour=discord.Colour.red()
                    ))

        await self.db.execute('INSERT INTO tickets VALUES(' + str(ticket.id) + ', ' + str(reaction_user.id) + ', true)')

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @has_ticket_permissions()
    async def add(self, ctx, member: discord.Member):
        av = self.bot.user.avatar_url
        try:
            r = await self.db.execute('SELECT 1 FROM tickets WHERE channel_id = ' + str(ctx.channel.id))
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

        await ctx.channel.set_permissions(member, send_messages=True, read_messages=True)
        await ctx.send(embed=discord.Embed(
            title=f"Added {member.name} to the ticket",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        ))

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @has_ticket_permissions()
    async def close(self, ctx):

        av = self.bot.user.avatar_url
        user = await self.db.execute("SELECT user_id FROM tickets WHERE channel_id = " + str(ctx.channel.id))
        user = self.bot.get_user(user[0][0])
        try:
            await self.db.execute('SELECT 1 FROM tickets WHERE channel_id = ' + str(ctx.channel.id))
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

        await asyncio.sleep(3)

        await self.db.execute('UPDATE tickets SET open = false WHERE channel_id = ' + str(ctx.channel.id))
        msg = await ctx.send(embed=closing)
        closed = discord.utils.get(ctx.guild.categories, id=tickets_archived_category_id)

        await ctx.channel.edit(
            name=f"Archived-{user.display_name}",
            topic=f"Ticket opened by {user.mention}. Closed by {ctx.author.mention}!",
            category=closed,
            reason="Ticket Closed."
        )

        # await ctx.channel.set_permissions(user, send_messages=True, read_messages=True)

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

    # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #

    @commands.command()
    @has_ticket_permissions()
    async def reopen(self, ctx):

        av = self.bot.user.avatar_url
        user = await self.db.execute("SELECT user_id FROM tickets WHERE open = false AND channel_id = " + str(ctx.channel.id))
        user = self.bot.get_user(user[0][0])
        try:
            result = await self.db.execute('SELECT 1 FROM tickets WHERE open = false AND channel_id = ' + str(ctx.channel.id))
            if not result:
                raise Exception()
        except Exception:
            not_ticket = em(
                title="Sorry!",
                description="Sorry! This channel isn't a ticket or a closed ticket. "
                            "Please use this command again in a closed ticket.",
                colour=discord.Colour.red(),
                timestamp=datetime.utcnow()
            )
            not_ticket.set_footer(
                icon_url=av,
                text="IsThicc Tickets"
            )
            return await ctx.send(embed=not_ticket)

        await self.db.execute('UPDATE tickets SET open = true WHERE channel_id = ' + str(ctx.channel.id))
        open = discord.utils.get(ctx.guild.categories, id=tickets_category_id)

        await ctx.channel.edit(
            name=f"Ticket-{user.display_name}",
            topic=f"Ticket opened by {user.mention}. Reopened by {ctx.author.mention}!",
            category=open,
            reason="Ticket Reopened."
        )

        await ctx.send(embed=em(
            title="Ticket reopened!",
            colour=discord.Colour.green(),
            timestamp=datetime.utcnow()
        ).set_footer(
            icon_url=av,
            text="IsThicc Tickets"
        ))

#
#
# # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # # #
#
#
def setup(bot):
    bot.add_cog(Tickets(bot))
