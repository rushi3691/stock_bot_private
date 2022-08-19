from bsedata.bse import BSE
import json
import aiofiles
from utils.others import aiohttp_client


class CustomBSE(BSE):
    async def updateScripCodes(self):
        """
        Download a fresh copy of the scrip code listing

        :returns: None
        """
        async with aiohttp_client.get("https://static.quandl.com/BSE+Descriptions/stocks.txt") as resp:
            r = await resp.text()

        stk = {x.split("|")[1][3:]: x.split("|")[0][:-11] for x in r.split("\n") if x != '' and x.split("|")[1][:3] == 'BOM'}
        stk.pop("CODE", None)
        indices = {x.split("|")[1]: x.split("|")[0] for x in r.split("\n") if x != '' and x.split("|")[1][:3] != 'BOM'}
        indices.pop("CODE", None)
        async with aiofiles.open("services/bse/stk.json", 'w+') as fl:
            await fl.write(json.dumps(stk))
        async with aiofiles.open('services/bse/indices.json', 'w+') as fl:
            await fl.write(json.dumps(indices))



    async def getScripCodes(self):
        """
        :returns: A dictionary with scrip codes as keys and company names as values
        """
        async with aiofiles.open('services/bse/stk.json', 'r') as fl:
            return json.loads(await fl.read())
