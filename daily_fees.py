import requests
import time
node = '127.0.0.1'
fees = 0
total_fees = 0
ndays = 0
prevdate = ''
last = requests.get('http://' + node + ':6869/blocks/height').json()['height']
print ("-" * 32)
print(str.center("Fees for the last 30 days", 32))
print
print ("   Date               Total fees")
print ("-" * 32)
try:
    for n in range(1, int(last / 100.0)):
        for block in reversed(requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, last - n * 100, last - (n - 1) * 100 - 1)).json()):
            txs = block['transactions']
            date = time.strftime('%m/%d/%Y', time.gmtime(block['timestamp']/1000.))
            for tx in txs:
                fees += float(tx['fee']) / 100000000
            if date!=prevdate and prevdate!='':
                print ("%10s    %18.8f" % (prevdate, fees))
                total_fees += fees
                fees = 0
                ndays += 1
                if ndays == 30:
                    raise
            prevdate = date
except:
    pass
average_dfees = total_fees / ndays
print ("-" * 32)
print ("        Total %18.8f" % total_fees)
print ("Daily average %18.8f" % average_dfees)