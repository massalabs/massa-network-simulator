from secp256k1 import PrivateKey
import base58
import varint
from blake3 import blake3


def get_bytes_compact(transaction):
    enc_sender_pub_key = base58.b58decode_check(transaction['content']['sender_public_key'])
    enc_fee = varint.encode(int(transaction['content']["fee"]))
    enc_expire_period = varint.encode(transaction['content']["expire_period"])
    enc_type_id = varint.encode(0)
    recipient_address = base58.b58decode_check(transaction['content']['op']['Transaction']["recipient_address"][1:])[1:]
    enc_amount = varint.encode(int(transaction['content']['op']['Transaction']['amount']))
    bytes_compact = enc_fee + enc_expire_period + enc_sender_pub_key + enc_type_id + recipient_address + enc_amount
    return bytes_compact

def create_transaction(sender_private_key, sender_public_key, fee, expire_period, recipient_address, amount):
    transaction = {"content": {"op": {"Transaction": {}}}}

    transaction['content']["sender_public_key"] = sender_public_key.decode("utf-8")
    transaction['content']["fee"] = fee
    transaction['content']["expire_period"] = expire_period
    transaction['content']['op']['Transaction']["recipient_address"] = recipient_address
    transaction['content']['op']['Transaction']['amount'] = amount
    transaction['signature'] = sign_transaction(transaction, sender_private_key).decode("utf-8")
    
    transaction['content']["fee"] = "{0:.9f}".format(transaction['content']["fee"] / 1e9)
    transaction['content']['op']['Transaction']['amount'] = "{0:.9f}".format(transaction['content']['op']['Transaction']['amount'] / 1e9)
    
    return transaction

def sign_transaction(transaction, private_key):
    # Compute bytes compact
    encoded_data = get_bytes_compact(transaction)

    # Hash
    encoded_data = blake3(encoded_data).digest()

    # Sign
    private_key = PrivateKey(privkey=base58.b58decode_check(private_key), raw=True)
    signature = private_key.schnorr_sign(encoded_data, bip340tag='', raw=True)
    # signature_b58 = base58.b58encode_check(private_key.ecdsa_serialize_compact(signature))
    signature_b58 = base58.b58encode_check(signature)
    return signature_b58


if __name__ == "main":
    transaction = {
        "signature": "2KqRFP6TXVcpyBxENFECfWFfhLJwmDrmzz3RJMSC5B1eqmTKip2VVS1ZazX2gFa8ELEDtBj4iyU4QeUMakikrNBbYsyza",
        "content": {
            "sender_public_key": "4vYrPNzUM8PKg2rYPW3ZnXPzy67j9fn5WsGCbnwAnk2Lf7jNHb",
            "fee": 1000,
            "expire_period": 310010,
            "op": {
                "Transaction": {
                    "recipient_address": "2PoZqccygydkQfwdLXJEvgdsf4kRV2RmeYSupT1gcQ4kedBDcF",
                    "amount": 1000
                }
            }
        }
    }

    from crypto import deduce_address, get_schnorr_pubkey

    privkey = PrivateKey(privkey=base58.b58decode_check("LGXe9RrR1QNSsSn8bAEgrsYM8WwX67oHLjGj6e19bCW9ZKo6p"), raw=True)
    pubkey = get_schnorr_pubkey(privkey)
    address = deduce_address(pubkey)

    print("private_key", base58.b58encode_check(privkey.private_key))
    print("public_key", base58.b58encode_check(get_schnorr_pubkey(privkey)))
    print("address", deduce_address(pubkey))

    # Sign transaction
    sign_transaction(transaction, privkey)
