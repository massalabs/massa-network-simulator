from secp256k1 import PrivateKey
import base58
import varint
from blake3 import blake3
from crypto import KeyPair, decode_pubkey_to_bytes

def get_bytes_compact(content):
    enc_fee = varint.encode(int(content["fee"]))
    enc_expire_period = varint.encode(content["expire_period"])
    enc_type_id = varint.encode(0)
    recipient_address = base58.b58decode_check(content['op']['Transaction']["recipient_address"][1:])[1:]
    enc_amount = varint.encode(int(content['op']['Transaction']['amount']))
    bytes_compact = enc_fee + enc_expire_period + enc_type_id + recipient_address + enc_amount
    return bytes_compact

def create_transaction(sender_private_key, creator_public_key, fee, expire_period, recipient_address, amount):

    content = {}
    content["fee"] = fee
    content["expire_period"] = expire_period
    content['op'] = {}
    content['op']['Transaction'] = {}
    content['op']['Transaction']["recipient_address"] = recipient_address
    content['op']['Transaction']['amount'] = amount

    transaction = {}
    transaction["creator_public_key"] = creator_public_key
    transaction["signature"] = sign_transaction(transaction["creator_public_key"], content, sender_private_key).decode("utf-8")
    transaction["serialized_content"] = get_bytes_compact(content)
    return transaction

def sign_transaction(public_key, content, private_key):
    # Compute bytes compact
    encoded_data = get_bytes_compact(content)
    enc_sender_pub_key = decode_pubkey_to_bytes(public_key)
    encoded_data = enc_sender_pub_key + encoded_data
    # Hash
    encoded_data = blake3(encoded_data).digest()

    # Sign
    keypair = KeyPair.from_secret_massa_encoded(private_key)
    signature = keypair.secret_key.sign(encoded_data)
    # signature_b58 = base58.b58encode_check(private_key.ecdsa_serialize_compact(signature))
    signature_b58 = base58.b58encode_check(signature)
    return signature_b58

