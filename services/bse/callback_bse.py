from .bse import (
    bseCode, checkBse
) 
from utils.logger import logger
from utils.actions import send_typing_action
from pyrogram import Client
from pyrogram.types import CallbackQuery
import asyncio
from utils.others import executor

async def bseCallback(c: Client, callback_query: CallbackQuery):
    data = callback_query.data
    func_code = int(data.split()[1])
    if func_code == 0 : 
        logger.info('func_code = 0')
        await bseNameCallback(c, callback_query)
    elif func_code == 1 : 
        logger.info('func_code = 1')
        await bseBestCallback(c, callback_query)
    elif func_code == 2 : 
        logger.info('func_code = 2')
        await bseWorstCallback(c, callback_query)


@send_typing_action
async def bseNameCallback(c: Client, callback_query: CallbackQuery):
    # query = update.callback_query
    data = callback_query.data.split()[0]
    await bseCode(c, callback_query, data)


@send_typing_action
async def bseBestCallback(c: Client, callback_query: CallbackQuery): 
    data = int(callback_query.data.split()[0])
    temp_bse = await checkBse()
    from services.bse.bse import bse_top_gainers
    if not bse_top_gainers:
        loop = asyncio.get_event_loop()
        bse_top_gainers = loop.run_in_executor(executor, temp_bse.topGainers)
    if bse_top_gainers:
        lastPrice = bse_top_gainers[data]['LTP']
        securityID = bse_top_gainers[data]['securityID']
        scripCode = bse_top_gainers[data]['scripCode']
        pChange = bse_top_gainers[data]['pChange']
        change = bse_top_gainers[data]['change']
        text = \
f"""
scripCode: `{scripCode}`
securityID: {securityID}
lastPrice: {lastPrice}
change: {change}
%change: {pChange}"""

        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text=text)
        return await callback_query.message.delete()
    else:
        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text="Some error occured at bseBestCallback!")
        return await callback_query.message.delete()

@send_typing_action
async def bseWorstCallback(c: Client, callback_query: CallbackQuery):
    global bse_top_losers, nse_fetch 
    data = int(callback_query.data.split()[0])
    temp_bse = await checkBse()
    from services.bse.bse import bse_top_losers
    if not bse_top_losers:
        loop = asyncio.get_event_loop()
        bse_top_losers = loop.run_in_executor(executor, temp_bse.topLosers)
    if bse_top_losers:
        lastPrice = bse_top_losers[data]['LTP']
        securityID = bse_top_losers[data]['securityID']
        scripCode = bse_top_losers[data]['scripCode']
        pChange = bse_top_losers[data]['pChange']
        change = bse_top_losers[data]['change']
        text = \
f"""
scripCode: `{scripCode}`
securityID: {securityID}
lastPrice: {lastPrice}
change: {change}
%change: {pChange}"""

        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text=text)
        return await callback_query.message.delete()
    else:
        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text="Some error occured at bseWorstCallback!")
        return await callback_query.message.delete()
