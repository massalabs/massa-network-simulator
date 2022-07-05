import numpy as np
import hashlib
import base58
import random
from blake3 import blake3
import varint
import ed25519

class KeyPair:
    def __init__(self, secret_key=None, public_key=None):
            self.secret_key = secret_key
            self.public_key = public_key
    
    def random():
        signing_key, verifying_key = ed25519.create_keypair()
        return KeyPair(secret_key=signing_key, public_key=verifying_key)

    def from_secret_massa_encoded(private: str):
        # Strip identifier
        private = private[1:]
        # Decode base58
        private = base58.b58decode_check(private)
        # Decode varint
        version = varint.decode_bytes(private)
        # Get rest (for the moment versions are little)
        secret_key = private[1:]
        # decode privkey
        secret_key = ed25519.keys.SigningKey(secret_key)
        public_key = secret_key.get_verifying_key()
        return KeyPair(secret_key=secret_key, public_key=public_key)

    def get_public_massa_encoded(self):
        return 'P' + base58.b58encode_check(varint.encode(0) + self.public_key.to_bytes()).decode("utf-8")

    def get_secret_massa_encoded(self):
        return 'S' + base58.b58encode_check(varint.encode(0) + self.secret_key.to_bytes()).decode("utf-8")

def decode_pubkey_to_bytes(pubkey):
    return base58.b58decode_check(pubkey[1:])[1:]

def deduce_address(pubkey):
    return 'A' + base58.b58encode_check(varint.encode(0) + blake3(pubkey.to_bytes()).digest()).decode("utf-8")

def get_address_thread(address):
    address_bytes = base58.b58decode_check(address[1:])[1:]
    return np.frombuffer(address_bytes, dtype=np.uint8)[0] / 8
