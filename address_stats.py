import requests
import math
import pandas as pd
import argparse
import threading

node = '127.0.0.1'
nthreads = 10

def blocks_reader(seq_from, seq_to, index):
    thread_blocks[index] = requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, seq_from, seq_to)).json()
    
parser = argparse.ArgumentParser(description='Statistics for Waves address')
parser.add_argument('address', type=str, help='waves address')
parser.add_argument('-b', '--blocks', action='store_true', help='show the list of blocks mined by the address')

args = parser.parse_args()
address = args.address

valid = requests.get('http://' + node + ':6869/addresses/validate/' + address).json()['valid']
if valid == False:
    print("Invalid address")
    exit(1)

total_balance = 0
total_fees = 0
mined_blocks = 0
txfields = { 
			'type' 				: '', 
			'id' 				: '', 
			'sender'			: '',
			'senderPublicKey'	: '',
			'recipient'			: '',
			'amount'			: '',
			'assetId'			: '',
			'name'				: '',
			'description'		: '',
			'quantity'			: '',
			'decimals'			: '',
			'reissuable'		: '',
			'fee'				: '',
			'feeAsset'			: '',
			'timestamp'			: '',
			'attachment'		: '',
			'signature'			: ''}

tmp=[]
mined_blocks=[]

last = requests.get('http://' + node + ':6869/blocks/height').json()['height']
df = pd.DataFrame(columns = txfields.keys())
for n in range(int(math.ceil(last / (nthreads * 100)))):
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
    	if block['generator'] == address:
    		total_fees += float(block['fee']) / 100000000
    		mined_blocks.append(block['height'])
        txs = block['transactions']
        for tx in reversed(txs):
            for key in txfields.keys():
                txfields[key] = ''
                try:
                    txfields[key] = tx[key]
                except:
                    pass
            tmp.append(txfields.values())
df = df.append(pd.DataFrame(tmp, columns = txfields.keys()), ignore_index=True)
try:
    address_balance = float(requests.get('http://' + node + ':6869/addresses/balance/' + address).json()['balance']) / 100000000
except:
    address_balance = 0
print("-" * 90)
print
print(str.center(("Statistics for address %s" % address), 90))
print
print("-" * 90)
print("")
print("                  %18.8f  Current balance" % address_balance)
print("                  %18.8f  Collected fees" % total_fees)
print("                        %12d  Mined blocks" % len(mined_blocks))
print("                        %12d  Sent transactions" % len(df[(df.sender==address) & (df.type==2)]))
print("                        %12d  Received transactions" % len(df[(df.recipient==address) & (df.type==2)]))
print("                  %18.8f  Total amount sent" % (sum(df[(df.sender==address) & (df.type==2)].amount) / 100000000.0))
print("                  %18.8f  Total amount received" % (sum(df[(df.recipient==address) & (df.type==2)].amount) / 100000000.0))
print

print "Assets balances:"
assets = requests.get('http://' + node + ':6869/assets/balance/' + address).json()['balances']
for asset in assets:
    asset_balance = asset['balance']
    decimals = asset['issueTransaction']['decimals']
    assetid = asset['assetId']
    name = asset['issueTransaction']['name'][:20].encode('ascii', 'ignore')
    amount = '{:.{prec}f}'.format(asset_balance / 10. ** decimals, prec=decimals)
    print ("%-44s %-20s %24s" % (assetid, name, amount))
print
if args.blocks:
    print("Mined blocks:")
    for row in range((len(mined_blocks) // 9) + 1):
        for col in range(9):
            n = row * 9 + col
            if n<len(mined_blocks):
                print("%8d " % mined_blocks[n]),
        print
    print
print("-" * 90) 
     
