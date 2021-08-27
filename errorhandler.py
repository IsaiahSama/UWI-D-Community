from discord.ext import commands

class ErrorHandler(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot

    async def on_command_error(self, ctx, error):
        await ctx.send(error, delete_after=10)

def setup(bot):
    bot.add_cog(ErrorHandler(bot))