import base58
import sha3
import pyblake2
import requests

FILLER = 'x'
CHAIN_BASE = '3P'
VALID_FIRST_CHARS = '123456789ABCDEFGHJKLMNPQR'
VALID_CHARS = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
NODE_URL = 'https://nodes.wavesnodes.com'

def hashChain(s):
    b = pyblake2.blake2b(s, digest_size=32).digest()
    return sha3.keccak_256(b).digest()

while True:
    base = raw_input("Base string : ")
    if len(base)>1 and base[0] not in VALID_FIRST_CHARS:
        print("The first character must be one of the followings: %s" % VALID_FIRST_CHARS)
    elif set(base) <= set(VALID_CHARS):
        base_address = CHAIN_BASE + base.ljust(33, FILLER)
        a=base58.b58decode(base_address)
        unhashedAddress = a[0:22]
        checkSum = hashChain(unhashedAddress)[0:4]
        address = base58.b58encode(unhashedAddress + checkSum)
        valid = requests.get('%s/addresses/validate/%s' % (NODE_URL, address)).json()['valid']
        print("Generated address : %-35s  %s" % (address, 'VALID' if valid else 'NOT VALID'))
    else:
        print("Valid characters are: %s" % VALID_CHARS)


