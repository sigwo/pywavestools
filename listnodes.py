import requests
import re
from ipwhois import IPWhois

node = 'nodes.wavesnodes.com'
peers = requests.get('https://' + node + '/peers/connected').json()['peers']
print("  #  Node name                      IP address    Country  Network              Network description")
print("-" * 120)
nodes_by_country = {}
for i, peer in enumerate(peers):
    match = re.search('.*\/(.*):.*', peer['address'])
    if match:
        ip = match.group(1)
        res = IPWhois(ip).lookup_whois()['nets'][0]
        country = ''
        net = ''
        descr = ''
        try:
            if res['country']:
                country = res['country']
            if res['name']:
                net = res['name']
            if res['description']:
                descr = res['description'].replace('\n', ' ')
        except:
            pass
        if country in nodes_by_country.keys():
            nodes_by_country[country] += 1
        else:
            nodes_by_country[country] = 1
        print ("%3d  %-30s %-15s  %-2s    %-20s %-40s" % (i + 1, peer['peerName'][:30], ip, country[:2], net[:20], descr[:40]))
print("-" * 120)
print
print("Country  # of nodes")
print("-" * 20)
for c in sorted(nodes_by_country.items(), key=lambda x: -x[1]):
    print ("  %-2s        %3d" % (c[0], c[1]))
print
print("-" * 120)

            