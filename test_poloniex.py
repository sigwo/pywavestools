import requests
import base58
import hashlib
import random
import struct
from datetime import datetime
import axolotl_curve25519 as curve
import os, pycurl, json

MATCHER_IP = "52.28.66.217"
MATCHER_PORT = "6886"
MATCHER_PUBLIC_KEY = "4oP8SPd7LiUo8xsokSTiyZjwg4rojdyXqWEq7NTwWsSU"
MATCHER_FEE = 1000000

MAX_TRADES = 100

POLONIEX_URL =  "https://poloniex.com/public?command=returnTradeHistory&currencyPair=BTC_"

traders = [{"pubkey": "BSnjDX6C5MdAJFRok1NjjmUXhMg6vDigEnF4Ee49FMJi", "privkey": "********************************************"},
           {"pubkey": "6UNgiZYHhVoqhZy6jEeqy3nMDk1DsRGpeTXJgCZTJNHW", "privkey": "********************************************"},
           {"pubkey": "4Rqx6BGNkGUxXT63oMTK3ZBcwJj7CmRWYheMvHaRFDHF", "privkey": "********************************************"},
           {"pubkey": "FQdqGA8voKpSCeJRBDmqoiqTE89M81kASDS5vD1LeihQ", "privkey": "********************************************"},
           {"pubkey": "FHo23swJaWBcGdDkbw4QQN2nHz3ZMzM8davFNEqJrjy6", "privkey": "********************************************"}]

coin_assets = {"ETH": "7svNYxtx1Fezky3cqD2w9cZRzvXQECjzsPUM3aqkAKH",
               "ETC": "7mfGow9YFndNcbWp5FUhvnDXWzhNpm1CSvhXcQ56CZJL",
               "XMR": "HC69tatQYm492MUN9dJ8PEmT5VMNcWYykBYCNcpkRwkg",
               "FCT": "7UuSpv1hEDaJ9ktXiFgUNVoQRbxpkgrFxzjJxHcLtC7h",
               "DASH": "7AZC3y7Ns4sTQt9ThY3SuVY8niUaNxkuG1Lpkv4wrR13"}

BTC_asset = "ENqgDWF2xr4kbrCTNiYN7xnvdvYXuuvaRTtGWV2b3XqY"

maxTimestamp = (datetime(2017, 1, 31) - datetime(1970, 1, 1)).total_seconds() * 1000


def postOrder(pubKey, privateKey, spendAssetId, receiveAssetId, price, amount):
    sData = base58.b58decode(pubKey) + base58.b58decode(MATCHER_PUBLIC_KEY) + "\1" + base58.b58decode(spendAssetId) + "\1" + base58.b58decode(receiveAssetId) + struct.pack(">Q", price) + struct.pack(">Q", amount) + struct.pack(">Q", maxTimestamp) + struct.pack(">Q", MATCHER_FEE)
    random64 = os.urandom(64)
    id = base58.b58encode(hashlib.sha256(sData).digest())
    signature = base58.b58encode(curve.calculateSignature(random64, base58.b58decode(privateKey), sData))

    data = json.dumps({
        "id": id,
        "sender": pubKey,
        "matcher": MATCHER_PUBLIC_KEY,
        "spendAssetId": spendAssetId,
        "receiveAssetId": receiveAssetId,
        "price": price,
        "amount": amount,
        "maxTimestamp": maxTimestamp,
        "matcherFee": MATCHER_FEE,
        "signature": signature
    })

    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://%s:%s/matcher/orders/place" % (MATCHER_IP, MATCHER_PORT))
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Accept: application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.perform()
    print
    print


prev_tid = {}
volume = {}
for i in coin_assets.keys():
    prev_tid[i] = 0
    volume[i] = 0

ntrades = 0

while ntrades < MAX_TRADES:
    for coin in coin_assets.keys():
        lastTrade = requests.get("%s%s" % (POLONIEX_URL, coin)).json()[0]
        tid = lastTrade['tradeID']
        if tid != prev_tid[coin] or prev_tid[coin] == 0:
            price = int(float(lastTrade['rate']) * 100000000)
            amount = int(float(lastTrade['amount']) * float(lastTrade['rate']) * 100000000)
            txtype = lastTrade['type']
            volume[coin] += amount
            maxTimestamp += 1
            ntrades += 1
            print ("%6d  %s  %-5s %5s %18d %18d" % (ntrades, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), coin, txtype, price, amount))
            print
            if txtype == 'buy':
                postOrder(traders[0]['pubkey'], traders[0]['privkey'], coin_assets[coin], BTC_asset, price, amount)
                postOrder(traders[1]['pubkey'], traders[1]['privkey'], BTC_asset, coin_assets[coin], price, amount)
            else:
                postOrder(traders[1]['pubkey'], traders[1]['privkey'], coin_assets[coin], BTC_asset, price, amount)
                postOrder(traders[0]['pubkey'], traders[0]['privkey'], BTC_asset, coin_assets[coin], price, amount)
            print ("Volumes (BTC):")
            print ("-" * 24)
            for i in coin_assets.keys():
                print ("%-5s %18.8f" % (i, volume[i] / 100000000.))
            print("-" * 80)
            random.shuffle(traders)
        prev_tid[coin] = tid

