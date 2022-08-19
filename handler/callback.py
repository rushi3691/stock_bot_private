from bot.client import bot
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery
from services.yf.callback_yf import yfCallback as yfc
from services.nse.callback_nse import nseCallback as nc
from services.bse.callback_bse import bseCallback as bc
from services.yf.graph.callback_graph import graphCallback as gfc


@bot.on_callback_query(filters.regex("^.*yf$"))
async def yfCallback(c: Client, callback_query: CallbackQuery):
    return await yfc(c, callback_query)

@bot.on_callback_query(filters.regex("^.*nse$"))
async def nseCallback(c: Client, callback_query: CallbackQuery):
    return await nc(c, callback_query)

@bot.on_callback_query(filters.regex("^.*bse$"))
async def bseCallback(c: Client, callback_query: CallbackQuery):
    return await bc(c, callback_query)

@bot.on_callback_query(filters.regex("^.*gf$"))
async def gfCallback(c: Client, callback_query: CallbackQuery):
    return await gfc(c, callback_query)