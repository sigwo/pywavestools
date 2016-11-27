import requests
import math
node = '127.0.0.1'
total_balance = 0
addresses = []
unique_addresses = []
top = 50    # 0 for all
last = requests.get('http://' + node + ':6869/blocks/height').json()['height']
for n in range(0, int(math.ceil(last / 100.0))):
    for block in requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, 1 + n * 100, min(last, (n + 1) * 100))).json():
        txs = block['transactions']
        for tx in txs:
            try:
                addresses.append(tx['recipient'])
            except:
                continue
for address in set(addresses):
    address_balance = float(requests.get('http://' + node + ':6869/addresses/balance/' + address).json()['balance']) / 100000000
    if address_balance>0:
        unique_addresses.append((address, address_balance))
print("-" * 64)
print(str.center(("Waves Rich List"), 64))
if(top>0):
    print(str.center(("Top %d" % top), 64))
print
print("  #    Address                                        Balance")
print("-" * 64)
pos = 0
for address in sorted(unique_addresses, key=lambda x: -x[1])[:top if top>0 else len(unique_addresses)]:
    total_balance += address[1]
    pos += 1
    print("%6d %-38s %18.8f " % (pos, address[0], address[1]))
print("-" * 64)
print("                                              %18.8f" % (total_balance))
     