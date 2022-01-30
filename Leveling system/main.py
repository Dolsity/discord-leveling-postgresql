import os
from dotenv import load_dotenv
import asyncpg
from discord.ext import commands, ipc
from databases.levels import *
import logging
import discord

class Fora(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        self.ipc = ipc.Server(self,secret_key = "Swas")

    # Greetings
    async def on_ready(self):
        print(f'Logged in as {bot.user} ({bot.user.id} | In {len(bot.guilds)} guilds')

        # Loads all /commands
        for filename in os.listdir('./commands'):
            if filename.endswith('.py'):
                bot.load_extension(f'commands.{filename[: -3]}')

    # Guild opn message XP
    async def on_message(self, message):
        await self.process_commands(message)

        if message.author.bot:
            return

        await increase_xp_guild(self.db, message)

owners = [795969792778698763] # 753869504009863275

bot = Fora(command_prefix=".")

# Database ready
async def connect_db():
    load_dotenv()
    password = os.getenv('PASSWORD')
    database_name = os.getenv('DATABASE_NAME')
    database_user = os.getenv('DATABASE_USER')
    bot.db = await asyncpg.create_pool(database = database_name, user = database_user, password = password)
    await create_tables(bot.db)
    print(f'Database connected')

# Logging
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# Loading data from .env file
load_dotenv()
token = os.getenv('TOKEN')
bot.loop.run_until_complete(connect_db())
bot.run(token, reconnect=True)