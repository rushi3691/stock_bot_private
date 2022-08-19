import asyncio
from concurrent.futures import ThreadPoolExecutor
from aiohttp import ClientSession


lock = asyncio.Lock()
executor = ThreadPoolExecutor(max_workers=10)
aiohttp_client = ClientSession()