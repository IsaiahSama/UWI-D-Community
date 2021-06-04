from discord.ext import commands

class EventHandler(commands.Cog):
    pass 

def setup(bot):
    bot.add_cog(EventHandler(bot))