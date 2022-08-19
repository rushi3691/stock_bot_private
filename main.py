import uvloop
uvloop.install()
from dotenv import load_dotenv
load_dotenv()
from utils.logger import logger
from bot.client import bot
from handler.handler import *
from handler.callback import *
from utils.others import *
from pyrogram import idle


if __name__ == '__main__':
    bot.start()
    idle()
    bot.stop()