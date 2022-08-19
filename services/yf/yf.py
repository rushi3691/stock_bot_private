from typing import Union
import json
# from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from utils.logger import logger
from utils.actions import send_typing_action
import pandas as pd
from pyrogram import Client
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup
from yahoo_fin.stock_info import get_data, tickers_sp500, tickers_nasdaq, tickers_other, get_quote_table
import yfinance as yf 
import aiofiles
import asyncio

tickers = pd.DataFrame() 


callback_codes = {
    '0': ['yfname'], 
}


def allCodes():
    global tickers
    if tickers.empty :
        tickers = tickers_nasdaq(True)
        data = json.dumps(dict(zip(tickers['Symbol'], tickers['Security Name'])), indent= 4)
        with open('services/yf/stock_codes.json','w') as file:
                file.write(data)
        
async def checkName(code: str) -> dict :
    names = {}
    async with aiofiles.open('services/yf/stock_codes.json','r') as file:
        code_file=json.loads(await file.read())
        for i in code_file:
            if code.lower() in str(code_file[i]).lower():
                names[i] = code_file[i]

    return names

def yfButtons(obj: dict, func_code: str, helpText: str = None ) -> InlineKeyboardMarkup:
    keyboard = []
    # checking if obj is dict or list
    # why????
    # if isinstance(obj,dict):
    for i in obj:
        callback_data = f"{i} {func_code} yf"
        keyboard.append([InlineKeyboardButton(obj[i], callback_data=callback_data)])

    reply_markup = InlineKeyboardMarkup(keyboard)
    return reply_markup

async def yfName(c: Client, msg: Message, stock_name: str):
    global tickers
    allCodes()
    if not tickers.empty:
        names = await checkName(stock_name)
        if names:
            reply_markup = yfButtons(names, 0)
            return await msg.reply('Search results:', reply_markup=reply_markup)
        else:
            text = f"{stock_name} not found"
            return await msg.reply(text)

async def yfCode(c: Client, msg: Message, stock_code: str):
    loop = asyncio.get_event_loop()
    ticker = yf.Ticker(stock_code)
    quote = await loop.run_in_executor(None, ticker.get_info)
    if 'shortName' in quote:
        text = \
f"""
Company: {quote['shortName']}
lastPrice: {quote['regularMarketPrice']}
dayHigh: {quote['dayHigh']}
dayLow: {quote['dayLow']}"""
        reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Show Graph", callback_data = f"{stock_code} 0 gf")]])
        return await msg.reply(text=text, reply_markup= reply_markup)
    else:
        text = f"""{stock_code} not found"""
        return await msg.reply(text=text)




def yfmessage(quote: dict, args: str = None) -> str :
    if quote:
        if len(quote)== 1 :
            data = f"""{args} not found"""
        else:
            data = \
f"""
Company: {quote['shortName']}
lastPrice: {quote['regularMarketPrice']}
dayHigh: {quote['dayHigh']}
dayLow: {quote['dayLow']}"""

    return data