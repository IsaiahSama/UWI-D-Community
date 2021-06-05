from os import getenv
from dotenv import load_dotenv
from bot import Setup

load_dotenv()
bot_setup = Setup()

bot = bot_setup.create_bot()
print("Bot was created")
bot_setup.load_extensions()
print("Extensions were loaded")
bot_setup.run(getenv("key"))
