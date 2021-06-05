import discord
from discord import Activity, ActivityType, Status
from discord.ext import commands
from discord.ext.commands.bot import Bot
from botdata import constants, extensions
import aiosqlite

class Setup:    
    def __init__(self, bot=None) -> None:
        """ Class responsible for setting up the bot instance"""
        self.bot = bot

    def create_bot(self) -> Bot:
        """ Creates an instance of a bot and returns it """
        intents = discord.Intents.all()
        bot = commands.Bot(command_prefix=constants["PREFIX"], intents=intents, case_insensitive=True)
        self.bot = bot
        return bot

    def load_extensions(self):
        """ Loads all extensions for the bot"""
        for extension in extensions:
            try:
                self.bot.load_extension(extension)
                print(f"{extension} has been loaded")
            except Exception as err:
                print(f"An error occurred when trying to load {extension}: {err}")

    def run(self, key):
        """ Runs the bot using the provided key 
        
        Arguments:
        key = The bot's token
        """
        try:
            self.bot.run(key)
        except Exception as err:
            print(f"Could not get the bot online: {err}")

    async def set_activity(self):
        """ Async function used to set the activity for the bot"""

        activity = Activity(name=constants["ACTIVITY_NAME"], type=ActivityType.listening)
        await self.bot.change_presence(activity=activity, status=Status.online)

    async def create_db(self):
        db = await aiosqlite.connect("uwidb.sqlite3")
        await db.execute("""CREATE TABLE IF NOT EXISTS GroupTable(
            GROUP_ID INTEGER UNIQUE PRIMARY KEY AUTOINCREMENT NOT NULL,
            OWNER_ID INTEGER NOT NULL,
            GROUP_NAME TEXT UNIQUE NOT NULL,
            MEMBERS TEXT);""")
        
        await db.commit()
        await db.close()
