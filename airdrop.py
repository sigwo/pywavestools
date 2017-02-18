import pywaves as pw
import argparse
import os.path

# pw.setNode("http://127.0.0.1:6869","testnet")

parser = argparse.ArgumentParser(description='Waves Airdrop Tool')
parser.add_argument('pkey', type=str, help='private key of the sending address')
parser.add_argument('asset', type=str, help='ID of the asset to distribute')
parser.add_argument('amount', type=str, help='amount of asset to send to each recipient')
parser.add_argument('file', type=str, help='file with the list of recipients')

args = parser.parse_args()
amount = int(args.amount)
filename = args.file

if amount <= 0:
    print("Amount must be > 0")
elif not os.path.exists(filename):
    print("File not found!")
else:
    myAddress = pw.Address(privateKey = args.pkey)
    myToken = pw.Asset(args.asset)
    with open(filename) as f:
        lines = f.readlines()
    for address in lines:
        myAddress.sendAsset(pw.Address(address.strip()), myToken, amount)
        print("Sent %d %s to %s" % (amount, myToken.assetId, address.strip()))

