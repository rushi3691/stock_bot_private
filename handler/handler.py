from bot.client import bot
from pyrogram import Client, filters
from pyrogram.types import Message
from config import *
from utils.actions import send_typing_action
from utils.logger import logger

from services.nse.nse import (
    nseCode, nseName, nseBest, nseWorst
)
from services.yf.yf import (
    yfName, yfCode
)

from services.bse.bse import (
    bseName, bseCode, bseBest, bseWorst
)

allowed_users = [1022633498, 1703528165] # allowed users

@bot.on_message(filters.regex("^/start$"))
@send_typing_action
async def start(c: Client, msg: Message):
    chat_id = msg.chat.id
    DB[chat_id] = DEFAULT_SERVICE
    logger.info(f"new user: {chat_id}")
    start_text = \
f"""
Welcome to stock-bot
use `/help` for basic help
use `/help service` for service related help """

    await msg.reply_text(start_text)

@bot.on_message(filters.regex("^/set_service \w+$"))
@send_typing_action
async def set_to(c: Client, msg: Message):
    global SERVICES, DB
    chat_id = msg.chat.id
    try:
        service = msg.text.split()[1].lower()
    except:
        return await msg.reply_text(" argument")

    if service in SERVICES and SERVICES[service]:
        # CURR_SERVICE = service
        DB[chat_id] = service
        text = f"""set to {service}\nuse /help {service} for help"""
    else:
        text = f"service not found or service not active"
    await msg.reply_text(text)

@bot.on_message(filters.regex("^/name_search \w+$"))
@send_typing_action
async def searchName(c: Client, msg: Message):
    global DB 
    chat_id = msg.chat.id
    try:
        ds = msg.text.split()
        stock_name = ' '.join(ds[1:]).lower()
    except:
        return await msg.reply(" an argument!")

    if not chat_id in DB:
        DB[chat_id] = DEFAULT_SERVICE
        logger.info(f"new user: {chat_id}")

    if DB[chat_id] == 'nse':
        await nseName(c, msg, stock_name)
        
    elif DB[chat_id] == 'bse':
        await bseName(c, msg, stock_name)
        
    elif DB[chat_id] == 'yfinance':
        await yfName(c, msg, stock_name)

@bot.on_message(filters.regex("^/code_search \w+$"))
@send_typing_action
async def searchCode(c: Client, msg: Message):
    global DB 
    chat_id = msg.chat.id
    try:
        ds = msg.text.split()
        stock_code = ds[1].upper()
    except:
        return await msg.reply(" an argument!")

    if not chat_id in DB:
        DB[chat_id] = DEFAULT_SERVICE
        logger.info(f"new user: {chat_id}")

    if DB[chat_id] == 'nse':
        await nseCode(c, msg, stock_code)
        
    elif DB[chat_id] == 'bse':
        await bseCode(c, msg, stock_code)
        
    elif DB[chat_id] == 'yfinance':
        await yfCode(c, msg, stock_code)

@bot.on_message(filters.regex("^/service$"))
@send_typing_action
async def currService(c: Client, msg: Message):
    global DB 
    chat_id = msg.chat.id
    if not chat_id in DB:
        DB[chat_id] = DEFAULT_SERVICE
        logger.info(f"new user: {chat_id}")

    text=DB[chat_id]
    await msg.reply(text=text)

@bot.on_message(filters.regex("^/help \w+$"))
@send_typing_action
async def help(c: Client, msg: Message):
    args = msg.text.split()
    text_help = None
    if len(args)>1:
        if args[1].lower() == 'nse':
            text_help = \
f"""
use `/set nse` to set current ervice to NSE
use `/nsebest` for best performing stocks
            \(service must be set to NSE\)
use `/nseworst` for worst performing stocks
            \(service must be set to NSE\)"""
        elif args[1].lower() == 'bse':
            text_help = \
f"""
use `/set bse` to set current service to BSE
use `/bsebest` for best performing stocks
            \(service must be set to BSE\)
use `/bseworst` for worst performing stocks
            \(service must be set to BSE\)"""

        elif args[1].lower() == 'yf':
            text_help = \
f"""
use `/set yf` to set current service to NASDAQ"""
        else:
            text_help = \
f"""
{args} not found"""
        await msg.reply(text=text_help)
    else:
        text_help = \
f"""
use `/searchCode code` to get info
use `/searchName name` to search stocks
use `/set service` to set default service
availabe services are
nse : for NSE
bse : for BSE
yfinance : for NASDAQ
default service is yfinance for NASDAQ
fuse `/help service` for service related help"""
        await msg.reply(text=text_help)



# @bot.on_message(filters.regex("^/unknown$"))
# @send_typing_action
# async def unknown(c: Client, msg: Message):
#     await msg.reply(text="Sorry, I didn't understand that command.")

# @bot.on_message(filters.regex("^/error$"))
# @send_typing_action
# async def service_down(c: Client, msg: Message):
#     await msg.reply(text="Can't process your command..\nService is down!")
