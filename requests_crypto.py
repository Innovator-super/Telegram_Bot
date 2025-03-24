import requests
import json

def get_eth_price():
    res =requests.get("https://api.coinlore.net/api/ticker/?id=80")
    res_json = json.loads(res.text[1:-1])
    return res_json["price_usd"]