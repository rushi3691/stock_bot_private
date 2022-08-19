from utils.logger import logger
from utils.actions import send_typing_action
from pyrogram.types import Message, CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from nsetools import Nse
import json
from typing import Union, Tuple
import aiofiles
import asyncio 
from utils.others import lock, executor
from bot.client import bot

nse_fetch: Nse = None
top_gainers = None
top_losers = None 

nse_codes_flag = False

callback_codes = {
    '0': ['nseName'], 
    '1': ['top_gainers'], 
    '2': ['top_losers'],
}


def get_top_gainers():
    return top_gainers

# checks if nse exists or not and 
# if it doesn't then creates nse
# done
async def checkNse():
    global nse_fetch, nse_codes_flag
    async with lock:
        if not nse_fetch:
            nse_fetch = Nse()
        if nse_codes_flag == False:
            await allCodes()
            nse_codes_flag = True
        return nse_fetch 

# writes all codes to stock_codes.json 
# done
async def allCodes():
    loop = asyncio.get_event_loop()
    all_stock_codes = await loop.run_in_executor(None, nse_fetch.get_stock_codes)
    stock_codes = json.dumps(all_stock_codes, indent=4)
    async with aiofiles.open('services/nse/stock_codes.json', 'w') as file:
        await file.write(stock_codes)


# check if search query is in the file 
# done
# ?? use redis
async def checkName(code: str) -> Tuple[dict, str]:
    names = {}
    async with aiofiles.open('services/nse/stock_codes.json','r') as file:
        code_file=json.loads(await file.read())
        for i in code_file:
            if code.lower() in code_file[i].lower():
                names[i] = code_file[i]

    return names


# universal function to create buttons 
# text is for replacing 'symbol'
# done
def nseButtons(obj: Union[dict, list], func_code: str, helpText: str = None ) -> InlineKeyboardMarkup:
    keyboard = []
    #checking if obj is dict or list
    if isinstance(obj,dict):
        for i in obj:
            callback_data = f"{i} {func_code} nse"
            keyboard.append([InlineKeyboardButton(obj[i], callback_data=callback_data)])
    else:
        for i in enumerate(obj):
            callback_data = f"{i[0]} {func_code} nse"
            keyboard.append([InlineKeyboardButton(i[1]['symbol'], callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup



async def nseName(c: Client, msg: Message, stock_name: str):
    global nse_fetch
    await checkNse()

    # if nse_fetch:
    names = await checkName(stock_name)
    if names:
        reply_markup = nseButtons(names, 0)
        return await msg.reply('Search results:', reply_markup=reply_markup)
    else:
        text = f"{stock_name} not found"
        return await msg.reply(text)


async def nseCode(c: Client, msg_or_query: Union[Message, CallbackQuery], stock_code: str):
    global nse_fetch
    await checkNse()
    # if nse_fetch:
    loop = asyncio.get_event_loop()
    quote = await loop.run_in_executor(executor, nse_fetch.get_quote, stock_code)
    text = nseMessage(quote, stock_code)
    if isinstance(msg_or_query, CallbackQuery):
        return await msg_or_query.edit_message_text(text)
    else:
        return await msg_or_query.reply(text)

def nseMessage(quote: str, args: str = None) -> str :
    if quote:
        data = \
f"""
companyName: {quote['companyName']}
lastPrice: {quote['lastPrice']}
dayHigh: {quote['dayHigh']}
dayLow: {quote['dayLow']}"""
    else:
        data = f"""{args} not found"""
    return data

@bot.on_message(filters.regex("^/nsebest$"))
@send_typing_action
async def nseBest(c: Client, msg: Message):
    global nse_fetch, top_gainers
    await checkNse()
    # if nse_fetch:
    loop = asyncio.get_event_loop()
    top_gainers = await loop.run_in_executor(executor, nse_fetch.get_top_gainers)
    reply_markup = nseButtons(top_gainers, 1)
    await msg.reply('Top Gainers:', reply_markup=reply_markup)

@bot.on_message(filters.regex("^/nseworst$"))
@send_typing_action
async def nseWorst(c: Client, msg: Message):
    global nse_fetch, top_losers
    await checkNse()
    # if nse_fetch:
    loop = asyncio.get_event_loop()
    top_losers = await loop.run_in_executor(executor, nse_fetch.get_top_losers)
    reply_markup = nseButtons(top_losers, 2)
    await msg.reply('Top Losers:', reply_markup=reply_markup)