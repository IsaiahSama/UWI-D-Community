import asyncio
import discord
from discord.ext import commands
from botdata import vc_to_tc, constants
from discord import PermissionOverwrite
from database import *
import aiosqlite
from aiohttp import ClientSession
from bs4 import BeautifulSoup as BS

class General(commands.Cog):

    """ Class with general commands available to all members """
    
    def __init__(self, bot) -> None:
        self.bot = bot

    in_vc = []

    @commands.command(brief="Creates a temporary text channel", help="Creates a temporary text channel to be used while in a voice channel")
    async def speakme(self, ctx):
        if not ctx.author.voice.channel:
            await ctx.send("You are not in a voice channel")
            return 

        channel = ctx.guild.get_channel(vc_to_tc[ctx.author.voice.channel.id])

        overwrites = channel.overwrites

        for member in ctx.author.voice.channel.members:
            overwrites[member] = PermissionOverwrite(view_channel=True)

        await channel.edit(overwrites=overwrites)
        await ctx.send(f"Press here to join the Text Channel for your Voice channel: {channel.mention}")
        self.in_vc.append(ctx.author.id)

    @commands.command(brief="Creates a group for you and fellow students", help="Used to create a group, so you and your fellow students can get together", usage="group_name")
    async def creategroup(self, ctx, *, group_name):
        can_create = True
        async with aiosqlite.connect("uwidb.sqlite3") as db:
            if await group_exists(db, group_name):
                await ctx.send("A group with this name already exists")
                can_create = False

            groups = await owner_groups(db, ctx.author.id)
            if len(groups) > 4:
                await ctx.send("You already own the max number of groups.")
                can_create = False

            if can_create:
                await create_group(db, group_name, ctx.author.id)
                await ctx.send(f"Successfully created group. View with {constants['PREFIX']}mygroups")

    @commands.command(brief="Used to invite someone into your group", help="Invites a fellow server member to join your group", usage="member group_name")
    async def invite(self, ctx, member:discord.Member, *, group_name):
        async with aiosqlite.connect("uwidb.sqlite3") as db:
            group = await owner_groups_by_name(db, group_name, ctx.author.id)
            if not group:
                await ctx.send("You do not own a group by that name")
                return
    
        message = await ctx.send(f"Hey {member.mention}, You have been invited to {group[2]} by {ctx.author.mention}. Press the ✔️ below to accept. The invite is valid for 1 hour")

        await message.add_reaction("✔️")

        def check(reaction, user):
            return str(reaction.emoji) == "✔️" and user == member

        try:
            _, _ = await self.bot.wait_for("reaction_add", check=check, timeout=60 * 60)
        except asyncio.TimeoutError:
            await ctx.send(f"{ctx.author.mention}, your invite to {member.mention} to join {group[2]} has expired.")
            return

        async with aiosqlite.connect("uwidb.sqlite3") as db:
            members = group[3]
            new_members = f"{members}, {member.id}"
            await update_members(db, group[0], new_members)
        
        await ctx.send(f"{member.mention} is now a member of {group[2]}")

    @commands.command(brief="Shows the list of groups that you are in", help="SHows all groups that you are in currently")
    async def mygroups(self, ctx):
        async with aiosqlite.connect("uwidb.sqlite3") as db:
            groups = await get_groups(db, ctx.author.id)
            if not groups:
                await ctx.send("You are not in any groups")
                return 

        group_names = [f"`{group[2]}`" for group in groups]
        await ctx.send(", ".join(group_names))
        
    @commands.command(brief="Displays the Calendar for the current academic year", help="Used to view the calendar for the current academic year")
    async def calendar(self, ctx, *, option=None):
        if not option:
            await ctx.send(f"Use `{constants['PREFIX']}calendar semester 1 / semester 2 / graduation` instead")
            return

        options = {"semester 1": 0, "semester 2": 1, "graduation": 2}

        if option.lower() not in options.keys():
            await ctx.send(f"That is not a valid option. Valid options are {', '.join(list(options.keys()))}")
            return

        to_send = []
        async with ClientSession() as session:
            async with session.get("https://www.cavehill.uwi.edu/calendar.aspx") as req:
                soup = BS(await req.text(), "html.parser")
                info = soup.select("tr")
                to_send = [x.text for x in info]
        
        if not to_send:
            await ctx.send("An error has seemingly occurred and the calendar is not available for me at this moment. Refer to: https://www.cavehill.uwi.edu/calendar.aspx")
            return False

        data = ''.join(to_send).split("\n\n\n")
        
        await ctx.send(f"```\n{data[options[option.lower()]]}```")

        
    # Listener for VC change

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None and before.channel is not None and member.id in self.in_vc:
            overwrites = before.channel.overwrites
            del overwrites[member]            
            await before.channel.edit(overwrites=overwrites)


def setup(bot):
    bot.add_cog(General(bot))