import requests
import math
import argparse

node = '127.0.0.1'
nthreads = 10

parser = argparse.ArgumentParser(description='Generate a JSON for all transactions per a given Waves address')
parser.add_argument('address', help='Waves address')


args = parser.parse_args()

    
last = requests.get('http://' + node + ':6869/blocks/height').json()['height']

json = []
for n in range(0, int(math.ceil(last / 100.0))):
    for block in reversed(requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, max(1, last - (n + 1) * 100 + 1), min(last, last - n * 100))).json()):
        for tx in reversed(block['transactions']):
            if 'sender' in tx.keys() and tx['sender'] == args.address:
                    json.append(tx)
            if 'recipient' in tx.keys() and tx['recipient'] == args.address:
                    json.append(tx)   
print str([json])

