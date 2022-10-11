import asyncio
# import uvloop
# uvloop.install()
from dotenv import load_dotenv
load_dotenv()
from utils.logger import logger
from bot.client import bot
from handler.handler import *
from handler.callback import *
from utils.others import *
from pyrogram import idle

# fastapi dependencies
from fastapi import FastAPI
import uvicorn
from uvicorn import Server
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi import Request



app = FastAPI()
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})



async def main():
    config = uvicorn.Config("main:app", host="0.0.0.0", port=8000, workers=1)
    await bot.start()
    server = Server(config = config)
    api = asyncio.create_task(server.serve())
    _bot = asyncio.create_task(idle())

    await asyncio.wait([api, _bot])
    await bot.stop()

if __name__ == "__main__":
    bot.run(main())
