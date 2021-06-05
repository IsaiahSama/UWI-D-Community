from discord.ext import commands
from discord import utils, PartialMessage
from botdata import channels, constants, selectable_roles_by_name, selcetable_roles_by_emoji
class EventHandler(commands.Cog):
    
    def __init__(self, bot) -> None:
        """ Class used for handling all Events"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.guild.get_channel(channels["WELCOME"]).send(f"Welcome {member.mention} to The UWI Discord Community. Here, the only rule is to be sensible. Enjoy your time, we look forward to learning with you. Be sure to go to {member.guild.get_channel(channels['ROLES']).mention} and select your roles")

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot: return
        if message.channel.id == channels["COUNTING"]:
            await self.handle_counting(message)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        await self.handle_reaction(payload)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        await self.handle_reaction(payload)

    # Functions
    async def handle_counting(self, message):
        """ Function which handles messages being sent in the counting channel.

        This function ensures the following:
        
        1) Messages sent in this channel are numbers
        2) The message sent in the channel is the number directly after the previous one.
        3) If the new message is not consecutive from the previous one, resets number counter to 0
        """
        if not message.content.isnumeric():
            await message.add_reaction("❌")
            await message.channel.send(f"{message.author.mention} doesn't seem to know what a number is.")
            await message.channel.send("0")
            return
        
        try:
            previous = await message.channel.history(limit=2).flatten()
        except:
            await message.delete()
            await message.channel.send("0")
            return 

        try:
            previous = previous[1]
        except IndexError:
            return
        
        if not previous.content.isnumeric():
            await previous.add_reaction("❌")
            await message.channel.send(f"{previous.author.mention} doesn't seem to know what a number is.")
            await message.channel.send("0")
            return

        prev_number = int(previous.content)
        current_number = int(message.content)

        print(prev_number)

        if (prev_number + 1) != current_number:
            await message.add_reaction("❌")
            await message.channel.send(f"{message.author.mention} doesn't seem to know how to count, and has messed up for everyone")
            await message.channel.send("0")
            return 
        
        await message.add_reaction("✔️")

    async def handle_reaction(self, payload):
        if payload.channel_id != channels["ROLES"]: return
        guild = utils.get(self.bot.guilds, id=constants["GUILD_ID"])
        user = guild.get_member(payload.user_id)

        if not user: return

        try:
            role = guild.get_role(selectable_roles_by_name[selcetable_roles_by_emoji[str(payload.emoji)]])
        except:
            partial_message = PartialMessage(channel=guild.get_channel(payload.channel_id), id=payload.message_id)
            await partial_message.remove_reaction(payload.emoji, user)
            return

        if payload.event_type == "REACTION_ADD":
            await self.handle_reaction_add(role, user)
        else:
            await self.handle_reaction_remove(role, user)

    async def handle_reaction_add(self, role, user):
        await user.add_roles(role)

    async def handle_reaction_remove(self, role, user):
        await user.remove_roles(role)

def setup(bot):
    bot.add_cog(EventHandler(bot))