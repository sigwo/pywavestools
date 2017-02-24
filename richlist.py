import requests
import argparse

NODE = 'http://127.0.0.1:6869'

parser = argparse.ArgumentParser(description='Waves Rich List')
parser.add_argument('-t', '--top', type=int, help='lists only the specified top positions')

args = parser.parse_args()
if args.top:
    top = args.top
else:
    top = -1

states = requests.get('%s/debug/state' % NODE).json()
print("-" * 64)
print(str.center("Waves Rich List", 64))
if top > 0:
    print(str.center("Top %d balances" % top, 64))
print("  #    Address                                      Balance")
print("-" * 64)
n = 0
total_balance = 0
for i in sorted(states.items(), key=lambda x: -x[1]):
    balance = i[1]
    if len(i[0]) == 35 and balance > 0:
        address = i[0]
        total_balance += balance
        n += 1
        print("%6d %-38s %18.8f " % (n, address, balance / 1e8))
        if n == top:
            break
print("-" * 64)
print("                                              %18.8f" % (total_balance / 1e8))
