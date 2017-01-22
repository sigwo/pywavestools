import base58
import struct
import time
import axolotl_curve25519 as curve
import os, pycurl, json

NODE_IP = "127.0.0.1"
NODE_PORT = "6869"

sender_pubKey = "9PlrmTwP5avWKa9jDCk2NqPWrrMTRK52kUZdAPPWcuMT"
sender_privKey = "********************************************"

amount_to_send = 10000
fee = 100000

asset = "PmLtPqiWdfvU4UkoLMPdyKCADYhGfNWgk54EpKpGKTar"

recipients =   ['3MxH81cdbN8ETFJhNe6zj2mq7VLjnfLNPaf',
                '3NAV3TBreBMoyrNjaQH3LAULFf7U14ihCXr',
                '3MznWmJ7FXhUEyeCf7EnvwPSD5k3PsGGXpQ',
                '3N1qQwcWsfAhFp3JrHmhtsdAuKq94C4D3B9',
                '3MtBSwDB1EwSpcMiZ3ijkSYWzwBb3qrmcLf',
                '3MvihbR3LcPjV6vucmEM4828szih3CUZqcr',
                '3MwabbmoYVrT1fMWDGhWbirEUB6piWw2N4D',
                '3MuSwLtURv4cKgbiwzsKSfMH96KoE93q8LX',
                '3N7dYVvQ5kvVDL6DCX7WKLbAfm7qwNu5UEi',
                '3MsEK9bZTnQnv9XCRJ66EiMhTBxcPq1GcsC',
                '3NBMFAZCTxZPv2tRuK11RuxBaFiW4otCY3q',
                '3MuQkUzQjTRLkjFfkfrzKTZJRXTDaRYzEKN',
                '3Mp7cvTrBEtAdZRfm3L2sSn6yxY8ySWvYRE',
                '3MyQoPPvPTqCZYucaSrKwAc5Z9nAwMnwLU8',
                '3MwyBeyCNogSr8D6TjKPK1D84kfbx7LnZjC',
                '3N9a1u65fPCCV2epHpAYj97FnjPefT17sPx',
                '3MuZJzFgW2BbFwXRkJa11yNnjFTD5TS5Fdk',
                '3MwgddLyq1qk1WAJoEmvtGDkYVf24tkP9p6',
                '3N1e9i4CUbSN7BGZ8W27mdvNzbch9fzLrMC',
                '3N3fDYYJADrpU9g4jVVa8Sy2Yr7GnTAtsR5']


def sendAsset(pubKey, privKey, recipient, assetId, amount, txfee):
    timestamp = int(time.time() * 1000)
    sData = '\4' + base58.b58decode(pubKey) + '\1' + base58.b58decode(assetId) + '\0' + struct.pack(">Q", timestamp) + struct.pack(">Q", amount) + struct.pack(">Q", txfee) + base58.b58decode(recipient) + '\0\0'
    random64 = os.urandom(64)
    signature = base58.b58encode(curve.calculateSignature(random64, base58.b58decode(privKey), sData))

    data = json.dumps({
        "assetId": assetId,
        "senderPublicKey": pubKey,
        "recipient": recipient,
        "amount": amount,
        "fee": txfee,
        "timestamp": timestamp,
        "attachment": "",
        "signature": signature
    })

    c = pycurl.Curl()
    c.setopt(pycurl.URL, "http://%s:%s/assets/broadcast/transfer" % (NODE_IP, NODE_PORT))
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/json', 'Accept: application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, data)
    c.perform()
    c.close()



for r in recipients:
    print r
    sendAsset(sender_pubKey, sender_privKey, r, asset, amount_to_send, fee)
    print
    print("-" * 100)