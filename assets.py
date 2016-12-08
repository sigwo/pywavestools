import requests
import math
import time
import argparse
import threading

node = '127.0.0.1'
nthreads = 10

def blocks_reader(seq_from, seq_to, index):
    thread_blocks[index] = requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, seq_from, seq_to)).json()

parser = argparse.ArgumentParser(description='Assets list for the Waves platform')
parser.add_argument('-d', '--days', type=int, help='number of days to search')
parser.add_argument('-a', '--assets', type=int, help='number of assets to show')
parser.add_argument('-t', '--with-txs', action='store_true', help='shows only assets with transactions')
parser.add_argument('-c', '--compact', action='store_true', help='compact view')

args = parser.parse_args()

if args.days:
    max_days = args.days
else: 
    max_days = -1

if args.assets:
    max_assets = args.assets
else: 
    max_assets = -1
    
ndays = 0
count = 0
last = requests.get('http://' + node + ':6869/blocks/height').json()['height']
prevdate = ''
asset_txs={}
block_with_first_asset = 236967
if args.compact:
    print ("   #    Asset ID                                      Name                                   Amount")
    print ("-" * 99)
else:
    print ("   #        Issue date       Issuer                               Asset ID                                      Name                 Description                                          Quantity Decimals               Amount   Tx count")
    print ("-" * 235)
try:
    for n in range(int(math.ceil((last - block_with_first_asset) / (nthreads * 100)) + 1)):
        thread_blocks = []
        thread=[]
        for t in range(nthreads):
            thread_blocks.append('')
            thread.append(threading.Thread(target=blocks_reader, args=(max(1, last - (n + 1) * (nthreads * 100) + t*100 + 1), last - n * (nthreads * 100) - ((nthreads * 100) - 100) + t*100, t)))
            thread[t].start()
        blocks=[]
        for t in range(nthreads):
            thread[t].join()
            blocks = blocks + thread_blocks[t]
        for block in reversed(blocks):
            txs = block['transactions']
            for tx in reversed(txs):
                date = time.strftime('%m/%d/%Y', time.gmtime(tx['timestamp']/1000.))
                if date!=prevdate:
                    if ndays == max_days:
                        raise
                    ndays +=1
                prevdate = date
                if tx['type']==3:
                    if count == max_assets:
                        raise
                    issue_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(tx['timestamp']/1000.))
                    issuer = tx['sender']
                    assetid = tx['assetId']
                    name = tx['name'][:20].encode('ascii', 'ignore')
                    description = tx['description'][:40].encode('ascii', 'ignore').replace('\n',' ')
                    qt = tx['quantity']
                    dec = tx['decimals']
                    amount = '{:.{prec}f}'.format(qt / 10. ** dec, prec=dec)
                    if tx['assetId'] in asset_txs:
                        txcount = asset_txs[tx['assetId']]
                    else:
                        txcount = 0
                    if not(args.with_txs) or (args.with_txs and txcount > 0):
                        count += 1
                        if args.compact:
                            print ("%6d  %-45s %-20s %24s" % (count, assetid, name, amount))
                        else:
                            print ("%6d  %-19s  %-35s  %-45s %-20s %-40s %20d   %2d %24s %10d" % (count, issue_time, issuer, assetid, name, description, qt, dec, amount, txcount))   
                elif tx['type']==4:
                    if tx['assetId'] in asset_txs:
                        asset_txs[tx['assetId']] += 1
                    else:
                        asset_txs[tx['assetId']] = 0
except:
    pass    
if args.compact:
    print ("-" * 99)
else:
    print ("-" * 235)