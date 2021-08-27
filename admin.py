from discord.ext import commands 
from main import bot_setup
from botdata import constants

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
        await bot_setup.create_db()
        print("Database was created")


    @commands.command(brief="Creates a text channel with the given name", help="Used to create a text channel with the name specified (If the channel name has in a space, put the entire thing in quotes)", usage="channel_name Optional[category_id]")
    @commands.has_guild_permissions(manage_channels=True)
    async def create_text_channel(self, ctx, channel_name, category_id:int=None):
        if category_id:
            try:
                channel = ctx.guild.get_channel(category_id)
            except:
                await ctx.send("Could not find a category with that ID")
                return
        else:
            channel = ctx.channel
        
        success = await channel.create_text_channel(channel_name)
        message = f"Created text channel with the name {success.name} with id {success.id}"
        if category_id:
            message += f" in {channel.name} with id {category_id}"
        
        await ctx.send(message)

    @commands.command(brief="Creates a voice channel with the given name", help="Used to create a voice channel with the name specified", usage="channel_name Optional[category_id]")
    @commands.has_guild_permissions(manage_channels=True)
    async def create_voice_channel(self, ctx, channel_name, category_id:int=None):
        if category_id:
            try:
                channel = ctx.guild.get_channel(category_id)
            except:
                await ctx.send("Could not find a category with that ID")
                return
        else:
            channel = ctx.guild
        
        success = await channel.create_voice_channel(channel_name)
        message = f"Created voice channel with the name {success.name} with id {success.id}"
        if category_id:
            message += f" in {channel.name} with id {category_id}"
        await ctx.send(message)

    @commands.command(brief="Creates a Category with the given name", help="Used to create a Category with the name specified", usage="category_name")
    @commands.has_guild_permissions(manage_channels=True)
    async def create_category(self, ctx, channel_name):
        success = await ctx.guild.create_category(channel_name)
        await ctx.send(f"Created Category with the name {success.name} and id of {success.id}")

    @commands.commnd(brief="Moves a text or voice channel to another category", help="Moves a text or voice channel (by id) to another category.", usage="id_of_channel id_of_category")
    @commands.has_guild_permissions(manage_channels=True)
    async def move_channel(self, ctx, channel_id:int, category_id:int):
        channel, category = ctx.guild.get_channel(channel_id), ctx.guild.get_channel(category_id)
        if not all([channel, category]):
            await ctx.send(f"One of the given ids do not match any current existing channels/categories. Use {constants['PREFIX']}id_for channel_name to get the id of any channel/category.")
            return

        await channel.edit(category=category)
        await ctx.send(f"Successfully moved {channel.name} to {category.name}.")

    @commands.command()
    @commands.is_owner()
    async def create_role(self, ctx, role_name):
        role = await ctx.guild.create_role(name=role_name)
        await ctx.send(f"Created {role.name} with an id of {role.id}")

    @commands.command()
    @commands.is_owner()
    async def send_message(self, ctx, *, message):
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command()
    @commands.is_owner()
    async def add_reactions(self, ctx, message_id:int, *, reactions):
        reactions = reactions.split(", ")
        message = await ctx.channel.fetch_message(message_id)

        for reaction in reactions:
            await message.add_reaction(reaction)

def setup(bot):
    bot.add_cog(Admin(bot))