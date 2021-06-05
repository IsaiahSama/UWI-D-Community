from discord.ext import commands
from botdata import vc_to_tc
from discord import PermissionOverwrite

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

    # Listener for VC change

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        if after.channel is None and before.channel is not None and member.id in self.in_vc:
            overwrites = before.channel.overwrites
            del overwrites[member]            
            await before.channel.edit(overwrites=overwrites)


def setup(bot):
    bot.add_cog(General(bot))