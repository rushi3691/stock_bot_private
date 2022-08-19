from pyrogram import Client 
from pyrogram.types import CallbackQuery

from utils.logger import logger
from utils.actions import send_typing_action
from .generator import graph


@send_typing_action
async def gfCode(c: Client, callback_query: CallbackQuery):
    try:
        # args = context.args[0]
        data = callback_query.data.split()
        code = data[0]
        period = data[1]
        # period = context.args[1].lower()
        img = graph(code, period)
        await callback_query._client.send_photo(chat_id=callback_query.message.chat.id, photo=open(img, 'rb'))
        return await callback_query.message.delete()
        # context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(img,'rb'))
    except Exception as e:
        text = "some error at gfCode"
        logger.error(e)
        await callback_query._client.send_message(chat_id=callback_query.message.chat.id, text=text)
        return await callback_query.message.delete()
        # context.bot.send_message(chat_id=update.effective_chat.id, text=text)