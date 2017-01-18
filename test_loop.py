import base58
import hashlib
import struct
from datetime import datetime
import axolotl_curve25519 as curve
import os, pycurl, json

MATCHER_IP = "52.28.66.217"
MATCHER_PORT = "6886"
MATCHER_PUBLIC_KEY = "4oP8SPd7LiUo8xsokSTiyZjwg4rojdyXqWEq7NTwWsSU"
MATCHER_FEE = 1000000

MAX_TRADES = 1000

pubKey1 = "8SjRZLEqCSg48Spxozxe2F5TD3A9jeEVn4npGpU7RmHy"
privateKey1 = "********************************************"

pubKey2 = "9HFW4eDJtDJXgDWKQvvUrDpiiYJrrNk2yqRATy9Ru8WA"
privateKey2 = "********************************************"

BTC_asset = "94Sj2mk6Dx3YuWLewTpQbrRF2NDG6P9Z1geNuTnxyzVB"
USD_asset = "E7tRrkP7ZDFVK6KJR2K5koLFn5XdDb91L3wqQMD8U9UD"

price = 125000000000L
amount = 100000000L

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

for i in range(MAX_TRADES):
    print i
    postOrder(pubKey1, privateKey1, BTC_asset, USD_asset, price, amount)
    postOrder(pubKey2, privateKey2, USD_asset, BTC_asset, price, amount)
    maxTimestamp += 1
