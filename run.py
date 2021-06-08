import logging
import sys
import os
from lib.bot import PalmtrwwPy
from sys import stdout
from dotenv import load_dotenv
from non_blocking_file_handler import NonBlockingFileHandler


rootlog = logging.getLogger()
rootlog.setLevel(logging.INFO)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(message)s")


file_handler = NonBlockingFileHandler("log.txt", encoding="utf-8")
file_handler.setFormatter(formatter)

console_logger = logging.getLogger("console")
console = logging.StreamHandler(stdout)
console.setFormatter(formatter)
console_logger.addHandler(console)

console_logger.info("Loading and starting the bot..")

load_dotenv()
bot = PalmtrwwPy()

bot.run(os.getenv("TOKEN"))