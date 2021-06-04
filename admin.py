from discord.ext import commands 
from main import bot_setup

class Admin(commands.Cog):
    
    def __init__(self, bot) -> None:
        self.bot = bot
        bot.loop.create_task(self.async_init())

    async def async_init(self):
        print("Waiting until ready")
        await self.bot.wait_until_ready()
        print("Ready")
        await bot_setup.set_activity()

def setup(bot):
    bot.add_cog(Admin(bot))