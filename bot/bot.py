import discord
import logging
from discord.ext import commands
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from pathlib import Path

logger = logging.getLogger(__name__)
console_logger = logging.getLogger("console")

class PalmtrwwPy(commands.Bot):
    def __init__(self):
        self.ready = False
        self.scheduler = AsyncIOScheduler()
        

        super().__init__(command_prefix="p.", chunk_guilds_at_startup=True, case_sensitive=True, intents=discord.Intents.all())

    def setup(self):
        for cog in Path("bot/cogs").glob("*.py"):
            cogpath = f"bot.cogs.{cog}"
            self.load_extension(cogpath)
            console_logger.info(f"Loaded {cogpath}")


    async def on_ready(self):
        console_logger.info(
            f"Successfully logged in as {self.user.name} ID:{self.user.id} \t"
            f"d.py version: {discord.__version__} \t"
            "Further logging output will go to log file.."
        )

        if not self.ready:
            await self.on_first_ready()
            self.ready = True

    async def on_first_ready(self):
        self.setup()
        bot_log_channel = self.get_channel(851232777433382913)
        await bot_log_channel.send(embed=discord.Embed(title=f"Bot restarted"))


    @staticmethod
    async def on_connect():
        logger.info("Connection to Discord established.")

    @staticmethod
    async def on_disconnect():
        logger.info("Connection to Discord lost.")

    