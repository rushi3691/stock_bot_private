from utils.logger import logger
from utils.actions import send_typing_action
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from bot.client import bot
# from bsedata.bse import BSE
from services.bse.custom_bse import CustomBSE as BSE
import json
from typing import Union, Tuple
# from services.bse.utils import GetScripCodes, UpdateScripCodes
import aiofiles
import asyncio
from utils.others import lock, executor



bse_fetch: BSE = None
bse_top_gainers = None
bse_top_losers = None 

bse_codes_flag = False

callback_codes = {
    '0': ['bseName'], 
    '1': ['bse_top_gainers'], 
    '2': ['bse_top_losers'],
}

# checks if nse exists or not and 
# if it doesn't then creates nse
async def checkBse():
    global bse_fetch, bse_codes_flag
    async with lock:
        if not bse_fetch:
            bse_fetch = BSE(update_codes = False)
        if bse_codes_flag == False:
            await bse_fetch.updateScripCodes()
            bse_codes_flag = True
        return bse_fetch 

# writes all codes to stock_codes.json 
async def allCodes():
    all_stock_codes = await bse_fetch.getScripCodes()  
    stock_codes = json.dumps(all_stock_codes, indent=4)
    async with aiofiles.open('services/bse/stock_codes.json', 'w') as file:
        await file.write(stock_codes)


# check if search query is in the file 
async def checkName(code: str) -> Tuple[dict, str]:
    names = {}
    async with aiofiles.open('services/bse/stk.json','r') as file:
        code_file=json.loads(await file.read())
        for i in code_file:
            if code.lower() in code_file[i].lower():
                names[i] = code_file[i]

    return names 


# universal function to create buttons 
# text is for replacing 'symbol'
def bseButtons(obj: Union[dict, list], func_code: str, helpText: str = None ) -> InlineKeyboardMarkup:
    keyboard = []
    #checking if obj is dict or list
    if isinstance(obj,dict):
        for i in obj:
            callback_data = f"{i} {func_code} bse"
            keyboard.append([InlineKeyboardButton(obj[i], callback_data=callback_data)])
    else:
        for i in enumerate(obj):
            callback_data = f"{i[0]} {func_code} bse"
            keyboard.append([InlineKeyboardButton(i[1]['securityID'], callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

@send_typing_action
async def bseName(c: Client, msg: Message, stock_name: str):
    global bse_fetch
    await checkBse()
    # if bse_fetch:
    names = await checkName(stock_name)
    if names:
        reply_markup = bseButtons(names, 0)
        return await msg.reply('Search results:', reply_markup=reply_markup)
    else:
        text = f"{stock_name} not found"
        return await msg.reply(text)


@send_typing_action
async def bseCode(c: Client, msg_or_query: Union[Message, CallbackQuery], stock_code: str):
    global bse_fetch
    await checkBse()

    loop = asyncio.get_event_loop()
    try:
        quote = await loop.run_in_executor(executor, bse_fetch.getQuote, stock_code)
    except IndexError:
        quote = None
    text = bseMessage(quote, stock_code)
    if isinstance(msg_or_query, CallbackQuery):
        await c.send_message(chat_id = msg_or_query.message.chat.id, text=text)
        return await msg_or_query.message.delete()
    else:
        return await msg_or_query.reply(text)


def bseMessage(quote: str, stock_code: str = None) -> str :
    if quote:
        data = \
f"""
companyName: {quote['companyName']}
currentValue: {quote['currentValue']}
dayHigh: {quote['dayHigh']}
dayLow: {quote['dayLow']}"""
    else:
        data = f"""{stock_code} not found"""
    return data

@bot.on_message(filters.regex("^/bsebest$"))
@send_typing_action
async def bseBest(c: Client, msg: Message):
    global bse_fetch, bse_top_gainers
    await checkBse()
    # if bse_fetch:
    loop = asyncio.get_event_loop()
    bse_top_gainers = await loop.run_in_executor(executor, bse_fetch.topGainers)
    reply_markup = bseButtons(bse_top_gainers, 1)
    await msg.reply('Top Gainers:', reply_markup=reply_markup)

@bot.on_message(filters.regex("^/bseworst$"))
@send_typing_action
async def bseWorst(c: Client, msg: Message):
    global bse_fetch, bse_top_losers
    await checkBse()
    # if bse_fetch:
    loop = asyncio.get_event_loop()
    bse_top_losers = await loop.run_in_executor(executor, bse_fetch.topLosers)
    reply_markup = bseButtons(bse_top_losers, 2)
    await msg.reply('Top Losers:', reply_markup=reply_markup)