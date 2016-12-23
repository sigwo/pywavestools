import requests
import socket
import re
import time
from ipwhois import IPWhois
import argparse

parser = argparse.ArgumentParser(description='List nodes of the Waves network')
parser.add_argument('-a', '--all', action='store_true', help='shows removed or temporary offline nodes')
parser.add_argument('-v', '--version', action='store_true', help='shows node versions')

args = parser.parse_args()

checked_nodes=[]

def getPeers(node):
    peers = []
    try:
        tmp_peers = []
        if node not in checked_nodes:
            checked_nodes.append(node)
            try:
                tmp_peers = [['connected'] + [[x for x in requests.get(node + '/peers/connected', timeout=0.5).json()['peers'] if x['declaredAddress'].find(':6863')==-1 and x['address'].find(':6863')==-1]]]
                print("Getting peers from %s" % node)
            except:
                pass
            if args.all:
                try:
                    tmp_peers = tmp_peers + [['all'] + [requests.get(node + '/peers/all', timeout=0.5).json()]]
                except:
                    pass
            if len(tmp_peers) > 0:
                peers = peers + tmp_peers
                for p in zip(*tmp_peers)[1][0]:
                    match = re.search('.*\/(.*):.*', p['address'])
                    if match:
                        ip = match.group(1)
                        peers = peers + getPeers('http://' + ip + ':6869')
    except:
        pass
    return peers

def getVersion(ip):
    version = '  -'
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(1)
        s.connect((ip, 6868))
        data = s.recv(1024)
        n = ord(data[ord(data[0]) + 13])
        version = "%d.%d.%d" % (ord(data[ord(data[0]) + 4]), ord(data[ord(data[0]) + 8]), ord(data[ord(data[0]) + 12]))
        s.close()
    except:
        pass
    return version

peers = getPeers('https://nodes.wavesnodes.com') + getPeers('http://127.0.0.1:6869')

nodes_by_country = {}

print("Getting IP networks info...")
nodes=[('','','','','', '')]
for group in zip(*sorted(peers, key=lambda x: x[0], reverse=True))[1]:
    for peer in group:
        match = re.search('.*\/(.*):.*', peer['address'])
        if match:
            ip = match.group(1)
            if ip not in zip(*nodes)[1]:
                try:
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
                    name = ''
                    try:
                        name = peer['peerName'][:30]
                    except:
                        try:
                            name = peer['nodeName'][:30]
                        except:
                            pass
                    try:
                        if name[0]=='<':
                            name = ''
                    except:
                        name = ''
                    lastseen = 'online'
                    if args.all:
                        try:
                            lastseen = time.strftime('%m/%d/%Y %H:%M:%S', time.gmtime(peer['lastSeen']/1000.))
                        except:
                            pass
                    version = ''
                    if args.version:
                        version = getVersion(ip)
                    nodes.append((name, ip, country[:2], net[:20], descr[:40], version, lastseen))
                    if country in nodes_by_country.keys():
                        nodes_by_country[country] += 1
                    else:
                        nodes_by_country[country] = 1
                except:
                    pass
                
nodes = nodes[1:]
print
print
line_length = 120
if args.all:
    line_length = 142
if args.version:
    line_length += 8
print("-" * line_length)
print("  #  Node name                      IP address    Country  Network              Network description                     "),
if args.version:
    print ("Version "),
if args.all:
    print(" Status/Last seen")
else:
    print
print("-" * line_length)

for i, node in enumerate(sorted(nodes, key=lambda x: x[2])):
    print ("%3d  %-30s %-15s  %-2s    %-20s %-40s " % (i + 1, node[0], node[1], node[2], node[3], node[4])),
    if args.version:
        print ("%-8s" % node[5]),
    if args.all:
        print ("%-19s" % node[6])
    else:
        print
    
print("-" * line_length)
print
print("Country  # of nodes")
print("-" * 20)
for c in sorted(nodes_by_country.items(), key=lambda x: -x[1]):
    print ("  %-2s        %3d" % (c[0], c[1]))
print("-" * 20)
print ("            %3d" % sum(nodes_by_country.values()))
print
print("-" * line_length)
