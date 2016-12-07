import requests
import math
import time
import argparse

parser = argparse.ArgumentParser(description='Assets list for the Waves platform')
parser.add_argument('-d', '--days', type=int, help='number of days to search')
parser.add_argument('-c', '--compact', action='store_true', help='compact view')

args = parser.parse_args()

if args.days:
    max_days = args.days
else: 
    max_days = -1
    
ndays = 0
node = '127.0.0.1'
count = 0
last = requests.get('http://' + node + ':6869/blocks/height').json()['height']
prevdate = ''
if args.compact:
    print ("   #    Asset ID                                      Name                                   Amount")
    print ("-" * 99)
else:
    print ("   #        Issue date       Issuer                               Asset ID                                      Name                 Description                                          Quantity Decimals               Amount")
    print ("-" * 224)
try:
    for n in range(1, int(last / 100.0)):
        for block in reversed(requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, last - n * 100, last - (n - 1) * 100 - 1)).json()):
            txs = block['transactions']
            for tx in txs:
                date = time.strftime('%m/%d/%Y', time.gmtime(tx['timestamp']/1000.))
                if date!=prevdate:
                    if ndays == max_days:
                        raise
                    ndays +=1
                prevdate = date
                if (tx['type']==3):
                    count += 1
                    issue_time = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(tx['timestamp']/1000.))
                    issuer = tx['sender']
                    assetid = tx['assetId']
                    name = tx['name'][:20].encode('ascii', 'ignore')
                    description = tx['description'][:40].encode('ascii', 'ignore').replace('\n',' ')
                    qt = tx['quantity']
                    dec = tx['decimals']
                    amount = '{:.{prec}f}'.format(qt / 10. ** dec, prec=dec)
                    if args.compact:
                        print ("%6d  %-45s %-20s %24s" % (count, assetid, name, amount))
                    else:
                        print ("%6d  %-19s  %-35s  %-45s %-20s %-40s %20d   %2d %24s" % (count, issue_time, issuer, assetid, name, description, qt, dec, amount))         
except:
    pass    
if args.compact:
    print ("-" * 99)
else:
    print ("-" * 224)