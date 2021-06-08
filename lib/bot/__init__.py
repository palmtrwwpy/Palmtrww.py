import discord
import logging
import os
import aiosqlite
from discord.ext import commands
from discord.ext.commands import when_mentioned_or
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from glob import glob
from ..db import db
from pretty_help import DefaultMenu, PrettyHelp


menu = DefaultMenu(page_left="⬅️", page_right="➡️", remove="❌", active_time=100)
ending_note = "The ending note from {ctx.bot.user.name}\nFor command {help.clean_prefix}{help.invoked_with}"


logger = logging.getLogger(__name__)
console_logger = logging.getLogger("console")




class PalmtrwwPy(commands.Bot):
    def __init__(self):
        self.ready = False
        self.scheduler = AsyncIOScheduler()
        self.COGS = [path.split(os.sep)[-1][:-3] for path in glob("./lib/cogs/*.py")]
        
        db.autosave(self.scheduler)
        super().__init__(command_prefix=["p!", "p."], chunk_guilds_at_startup=True, case_sensitive=True, intents=discord.Intents.all(), help_command = PrettyHelp(menu=menu, ending_note=ending_note))

    def setup(self):
        for cog in self.COGS:
            self.load_extension(f"lib.cogs.{cog}")
            print(f"[COGS] {cog} cog loaded!")

        


    async def on_ready(self):
        console_logger.info(
            f"Successfully logged in as {self.user.name} ID:{self.user.id} \t"
            f"d.py version: {discord.__version__} \t"
            "Further logging output will go to log file.."
        )

        if not self.ready:
            self.scheduler.start()
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

    