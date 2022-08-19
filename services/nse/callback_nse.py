import asyncio
from re import A
from .nse import (
    checkNse
) 
from utils.logger import logger
from utils.actions import send_typing_action
from utils.others import executor
from pyrogram import Client
from pyrogram.types import CallbackQuery
from services.nse.nse import nseCode



async def nseCallback(c: Client, callback_query: CallbackQuery):
    data = callback_query.data
    func_code = int(data.split()[1])
    if func_code == 0 : 
        logger.info('func_code = 0')
        return await nseNameCallback(c, callback_query)
    elif func_code == 1 : 
        logger.info('func_code = 1')
        return await nseBestCallback(c, callback_query)
    elif func_code == 2 : 
        logger.info('func_code = 2')
        return await nseWorstCallback(c, callback_query)

@send_typing_action
async def nseNameCallback(c: Client, callback_query: CallbackQuery):
    data = callback_query.data.split()[0]
    await nseCode(c, callback_query, data)

@send_typing_action
async def nseBestCallback(c: Client, callback_query: CallbackQuery): 
    data = int(callback_query.data.split()[0])
    temp_nse = await checkNse()
    # from services.nse.nse import top_gainers

    # if not top_gainers:
    loop = asyncio.get_event_loop()
    top_gainers = await loop.run_in_executor(executor, temp_nse.get_top_gainers)
    if top_gainers:
        highPrice = top_gainers[data]['highPrice']
        lowPrice = top_gainers[data]['lowPrice']
        lastPrice = top_gainers[data]['ltp']
        symbol = top_gainers[data]['symbol']
        text = \
f"""
stockSymbol: `{symbol}`
lastPrice: {lastPrice}
highPrice: {highPrice}
lowPrice: {lowPrice}"""

        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text=text)
        return await callback_query.message.delete()
        # return await callback_query.edit_message_text(text=text)
    else:
        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text="Some error occured at nseBestCallback!")
        return await callback_query.message.delete()

@send_typing_action
async def nseWorstCallback(c: Client, callback_query: CallbackQuery):
    data = int(callback_query.data.split()[0])
    temp_nse = await checkNse()
    from services.nse.nse import top_losers
    if not top_losers:
        loop = asyncio.get_event_loop()
        top_losers = await loop.run_in_executor(executor, temp_nse.get_top_losers)
    if top_losers:
        highPrice = top_losers[data]['highPrice']
        lowPrice = top_losers[data]['lowPrice']
        lastPrice = top_losers[data]['ltp']
        symbol = top_losers[data]['symbol']
        text = \
f"""
stockSymbol: `{symbol}`
lastPrice: {lastPrice}
highPrice: {highPrice}
lowPrice: {lowPrice}"""

        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text=text)
        return await callback_query.message.delete()
        
        # return await callback_query.edit_message_text(text=text)
    else:
        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text="Some error occured at nseWorstCallback!")
        return await callback_query.message.delete()
