import requests
import math
node = '127.0.0.1'
nblocks = 10000
total_balance = 0
total_fees = 0
generators = []
unique_generators = []
last = requests.get('http://' + node + ':6869/blocks/height').json()['height']
for n in range(0, int(math.ceil(nblocks / 100.0))):
    for block in requests.get('http://%s:6869/blocks/seq/%d/%d' % (node, last - nblocks + n * 100, min(last, last - nblocks + (n + 1) * 100 - 1))).json():
        generators.append((str(block['generator']), float(block['fee']) / 100000000))
for generator in set([x[0] for x in generators]):
    fees = sum(g[1] for g in filter(lambda x: x[0] == generator, generators))
    count = sum(1 for g in filter(lambda x: x[0] == generator, generators))
    total_fees += fees
    generator_balance = float(requests.get('http://' + node + ':6869/consensus/generatingbalance/' + generator).json()['balance']) / 100000000
    unique_generators.append((generator, generator_balance, count, fees))
    total_balance += generator_balance
print("-" * 90)
print(str.center(("List of generators for the past %d blocks" % nblocks), 90))
print
print("                                                   Current     Current    Mined  Collected")
print(" #  Generator                                      balance       share   blocks       fees")
print("-" * 90)
for i, generator in enumerate(sorted(unique_generators, key=lambda x: -x[1])):
   print("%3d %-38s %18.8f  %6.2f%% %8d %10.3f" % (i + 1, generator[0], generator[1], generator[1] / total_balance * 100, generator[2], generator[3]))
print("-" * 90)
print("                                           %18.8f                   %10.3f" % (total_balance, total_fees))
     
