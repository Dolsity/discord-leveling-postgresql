from os import getenv
from dotenv import load_dotenv
import asyncpg
from nextcord.ext import commands
from utils import increase_xp_guild, create_tables, bot_owner_ids, bot_prefix
import nextcord
from nextcord import Intents
from extensions import initial_extensions

    
class Bot(commands.Bot):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

    async def on_message(self, message):
        await self.process_commands(message)

        if message.author.bot:
            return

        await increase_xp_guild(self.db, message)

intents = nextcord.Intents.default()
intents.members = True
intents.message_content = True


bot = Bot(command_prefix=bot_prefix, owner_ids = set(bot_owner_ids), intents=intents, case_insensitive=True)

@bot.event
async def on_ready():
    print(
        f'Logged in as {bot.user} ({bot.user.id}) ({nextcord.__version__})'
    )

# Database ready
async def connect_db():
    load_dotenv()
    password = getenv('PASSWORD')
    database_name = getenv('DATABASE_NAME')
    database_user = getenv('DATABASE_USER')
    bot.db = await asyncpg.create_pool(database = database_name, user = database_user, password = password)
    await create_tables(bot.db)
    print(f'Database connected')

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)

bot.loop.run_until_complete(connect_db())
bot.run(getenv('TOKEN'), reconnect=True)