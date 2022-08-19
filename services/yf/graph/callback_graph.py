from utils.logger import logger
from pyrogram import Client
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from utils.actions import send_typing_action
# from services.yf.graph.generator import graph
from services.yf.graph.gf import graph
from bot.client import bot
import asyncio
from utils.others import executor
import os
# ticker_code = None

async def graphCallback(c: Client, callback_query: CallbackQuery):
    # global ticker_code
    logger.info('in graphCallback')
    data = callback_query.data.split()
    func_code = int(data[1])
    if func_code == 0: 
        company_code = data[0]
        logger.info('func_code = 0')
        await graphPeriod(c, callback_query, company_code)
    elif func_code == 1: 
        logger.info('func_code = 1')
        await graphGenCallback(c, callback_query)

@send_typing_action
async def graphPeriod(c: Client, callback_query: CallbackQuery, company_code: str):
    logger.info('in graphPeriod')
    keyboard = [
        [InlineKeyboardButton("1 month",callback_data= f"1m 1 {company_code} gf")],
        [InlineKeyboardButton("1 year",callback_data= f"1y 1 {company_code} gf")],
        [InlineKeyboardButton("5 year",callback_data= f"5y 1 {company_code} gf")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text="Choose duration", reply_markup=reply_markup)
    return await callback_query.message.delete()
    # context.bot.send_message(chat_id=update.effective_chat.id, text="Choose duration", reply_markup= reply_markup)
    # query.message.delete()
    # query.edit_message_text("Choose duration: ", reply_markup= reply_markup)

    
@send_typing_action
async def graphGenCallback(c: Client, callback_query: CallbackQuery):
    logger.info('in graphGenCallback')
    # query = update.callback_query
    data = callback_query.data.split()
    period = data[0]
    ticker_code = data[2]
    logger.info(f"{period} {ticker_code}")
    loop = asyncio.get_event_loop()
    img = await loop.run_in_executor(executor, graph, ticker_code, period, callback_query.message.chat.id)
    # img = graph(ticker_code, period, callback_query.message.chat.id)
    await callback_query._client.send_photo(chat_id=callback_query.message.chat.id, photo=open(img, 'rb'))
    await callback_query.message.delete()
    os.remove(img)
    # query.message.delete()
    # context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img,'rb'))
    