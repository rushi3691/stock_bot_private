import requests 
import json 
import aiohttp

async def UpdateScripCodes():
    """
    Download a fresh copy of the scrip code listing

    :returns: None
    """
    r = requests.get("https://static.quandl.com/BSE+Descriptions/stocks.txt")
    stk = {x.split("|")[1][3:]: x.split("|")[0][:-11] for x in r.text.split("\n") if x != '' and x.split("|")[1][:3] == 'BOM'}
    stk.pop("CODE", None)
    indices = {x.split("|")[1]: x.split("|")[0] for x in r.text.split("\n") if x != '' and x.split("|")[1][:3] != 'BOM'}
    indices.pop("CODE", None)
    f_stk = open('services/bse/stk.json', 'w+')
    f_stk.write(json.dumps(stk))
    f_stk.close()
    f_indices = open('services/bse/indices.json', 'w+')
    f_indices.write(json.dumps(indices))
    f_indices.close()


def GetScripCodes():
    """
    :returns: A dictionary with scrip codes as keys and company names as values
    """
    f = open('services/bse/stk.json', 'r')
    return json.loads(f.read())