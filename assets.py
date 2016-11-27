import requests
import math
node = '127.0.0.1'
count = 0
last = requests.get('http://' + node + ':6869/blocks/height').json()['height']
print ("   #   Asset ID                                     Name                   Quantity")
print ("-" * 83)
for n in range(0, int(math.ceil(last/100.0))):
    for block in requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, 1 + n * 100, min(last, (n + 1) * 100))).json():
        txs = block['transactions']
        for tx in txs:
            if (tx['type']==3):
                count += 1
                print ("%6d %-40s %-20s %10d" % (count, tx['assetId'], tx['name'], tx['quantity']))
print ("-" * 83)