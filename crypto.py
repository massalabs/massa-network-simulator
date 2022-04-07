import numpy as np
import hashlib
import base58
import random


def deduce_address(pubkey):
    m = hashlib.sha256()
    m.update(pubkey)
    return base58.b58encode_check(m.digest())

def get_address_thread(address):
    address_bytes = base58.b58decode_check(address)
    return np.frombuffer(address_bytes, dtype=np.uint8)[0] / 8
    
    

def random_address():
    m = hashlib.sha256()
    m.update(bytearray(random.getrandbits(8) for _ in range(10)))
    return base58.b58encode_check(m.digest()).decode("utf-8")
