from discord.ext import commands
from botdata import channels
class EventHandler(commands.Cog):
    
    def __init__(self, bot) -> None:
        """ Class used for handling all Events"""
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        await member.guild.get_channel(channels["WELCOME"]).send(f"Welcome {member.mention} to The UWI Discord Community. Here, the only rule is to be sensible. Enjoy your time, we look forward to learning with you.")

def setup(bot):
    bot.add_cog(EventHandler(bot))