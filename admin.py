from discord.ext import commands 
from main import bot_setup

class Admin(commands.Cog):
    
    """Contains commands for admins and moderators. Only Moderator commands are displayed here """

    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.async_init())

    async def async_init(self):
        print("Waiting until ready")
        await self.bot.wait_until_ready()
        print("Ready")
        await bot_setup.set_activity()

    @commands.command()
    @commands.is_owner()
    async def create_role(self, ctx, role_name):
        await ctx.guild.create_role(name=role_name)
        await ctx.send(f"Created {role_name}")

    @commands.command(brief="Creates a text channel with the given name", help="Used to create a text channel with the name specified", usage="channel_name Optional[category_id]")
    @commands.has_guild_permissions(manage_channels=True)
    async def create_text_channel(self, ctx, channel_name, category_id:int=None):
        if category_id:
            channel = ctx.guild.get_channel(category_id)
        else:
            channel = ctx.channel
        
        success = await channel.create_text_channel(channel_name)
        await ctx.send(f"Created text channel with the name {success.name}")

    @commands.command(brief="Creates a voice channel with the given name", help="Used to create a voice channel with the name specified", usage="channel_name Optional[category_id]")
    @commands.has_guild_permissions(manage_channels=True)
    async def create_voice_channel(self, ctx, channel_name, category_id:int=None):
        if category_id:
            channel = ctx.guild.get_channel(category_id)
        else:
            channel = ctx.guild
        
        success = await channel.create_voice_channel(channel_name)
        await ctx.send(f"Created voice channel with the name {success.name}")

    @commands.command(brief="Creates a Category with the given name", help="Used to create a Category with the name specified", usage="category_name")
    @commands.has_guild_permissions(manage_channels=True)
    async def create_category(self, ctx, channel_name):
        success = await ctx.guild.create_category(channel_name)
        await ctx.send(f"Created Category with the name {success.name} and id of {success.id}")


def setup(bot):
    bot.add_cog(Admin(bot))