import requests
import argparse

parser = argparse.ArgumentParser(description='Waves Asset Rich List')
parser.add_argument('asset', type=str, help='asset id')

args = parser.parse_args()
assetId = args.asset

node = '127.0.0.1'

try:
    issuetx = requests.get('http://' + node + ':6869/transactions/info/%s' % assetId).json()
except:
    print("Asset not found!")
if issuetx['id'] == assetId:
    assetName = str(issuetx['name'])
    assetDec = issuetx['decimals']
    states = requests.get('http://' + node + ':6869/debug/state').json()
    print("-" * 64)
    print(str.center(("%s Rich List") % assetName, 64))
    print
    print("  #    Address                                        Balance")
    print("-" * 64)
    n = 0
    total_balance = 0
    for i in sorted(states.items(), key=lambda x: -x[1]):
        balance = i[1]
        if i[0][-len(assetId):] == assetId and balance > 0:
            address = i[0][:35]
            total_balance += balance
            n += 1
            balance = ("%%18.%df" % assetDec) % (balance / 10.**assetDec)
            print("%6d %-38s %18s " % (n, address, balance))
    print("-" * 64)
    total_balance = ("%%18.%df" % assetDec) % (total_balance / 10.**assetDec)
    print("                                            %20s" % (total_balance))

     