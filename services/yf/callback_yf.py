from .yf import (
    yfmessage
)

from utils.actions import send_typing_action
from utils.logger import logger
import yfinance as yf 
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client
from utils.logger import logger
import asyncio
from utils.others import executor


@send_typing_action
async def yfCallback(c: Client, callback_query: CallbackQuery):
    company_code = callback_query.data.split()[0]
    # logger.info(data)
    loop = asyncio.get_event_loop()
    ticker = yf.Ticker(company_code)
    quote = await loop.run_in_executor(executor, ticker.get_info)
    # quote = yf.Ticker(company_code).info
    text = yfmessage(quote)
    logger.info(f"yfCallback: {company_code}")
    reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Show Graph", callback_data = f"{company_code} 0 gf")]])
    await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text=text, reply_markup=reply_markup)
    return await callback_query.message.delete()
    # return await callback_query.message.edit_text(text, reply_markup=reply_markup)
    # query.message.edit_text(text, reply_markup= reply_markup)