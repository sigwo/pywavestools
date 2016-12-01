import requests
import re
from ipwhois import IPWhois

node = 'nodes.wavesnodes.com'
peers = requests.get('https://' + node + '/peers/connected').json()['peers']
print("  #   Node name                     IP address    Country  Network              Network description")
print("-" * 120)
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
        print ("%3i  %-30s %-15s  %-2s    %-20s %-40s" % (i + 1, peer['peerName'][:30], ip, country[:2], net[:20], descr[:40]))
print("-" * 120)

            