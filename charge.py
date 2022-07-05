import base58
import requests
import json
import numpy as np
import time
import sys
from multiprocessing import Pool

from transactions import create_transaction
from crypto import KeyPair, deduce_address, get_address_thread
from secp256k1 import PrivateKey

def get_current_period():
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "get_status",
        "id": 0,
        "params": []
    })
    response = requests.post("http://localhost:33032/", data=payload, headers=headers)
    return response.json()['result']['last_slot']['period']

def send_tx_list(tx_list):
    headers = {'Content-type': 'application/json'}
    payload = json.dumps({
        "jsonrpc": "2.0",
        "method": "send_operations",
        "id": 0,
        "params": [tx_list]
    })
    return requests.post('http://localhost:33032/', data=payload, headers=headers)


senderkey_faucet = KeyPair.from_secret_massa_encoded("S129yYZnj3hrAsMW263uZitJKp9bBm1oF3Z4v2gqAf7KANQKAf2Q")
print(senderkey_faucet.get_secret_massa_encoded())

def get_wallet(seed):
    np.random.seed(seed)
    wallet = [None] * 32
    address_in_all_thread = None not in wallet
    while not address_in_all_thread:
        keypair = KeyPair.random()
        address = deduce_address(keypair.public_key)
        thread = int(get_address_thread(address))
        if wallet[thread] is None:
            w = {
                'private_key' : keypair.get_secret_massa_encoded(),
                'public_key' : keypair.get_public_massa_encoded(),
                'address' : address
                }
            wallet[thread] = w
        address_in_all_thread = None not in wallet
    return wallet
    
wallet = get_wallet(0)

for i in range(32):
    print("Address in thread", i, ":", wallet[i]["address"])

#print(get_balances([w["address"] for w in wallet]))


def credit_wallet():
    tx_list = []
    for w in wallet:
        sender_private_key = senderkey_faucet.get_secret_massa_encoded()
        sender_public_key = senderkey_faucet.get_public_massa_encoded()
        fee = 0
        print("getting period")
        expire_period = get_current_period() + 8
        print(expire_period)
        recipient_address = w["address"]
        amount = 10000 * 1000000000
        print("create tx")
        tx = create_transaction(sender_private_key, sender_public_key, fee, expire_period, recipient_address, amount)
        print(tx)
        tx_list.append(tx)
    print("sending...")
    print(send_tx_list(tx_list).json())


def create_one_tx(i, shift, expire_period):
    #i, shift, expire_period = args
    tau = np.random.randint(32)
    #print(tau)
    keypair = KeyPair.from_secret_massa_encoded(wallet[tau]["private_key"])
    sender_private_key = keypair.get_secret_massa_encoded()
    sender_public_key = keypair.get_public_massa_encoded()
    fee = 0
    recipient_address = "A18dEoYk7mW2QXM19qmY7wqAjzqxC3mhVuhqhwCoueJzfvBMhLQ"
    amount = (i+1+shift) * 1
    return create_transaction(sender_private_key, sender_public_key, fee, expire_period, recipient_address, amount)


def send_thread(args):
    worker, txps, global_shift = args
    np.random.seed()
    expire_period = get_current_period() + 8
    batch_size = 100
    n = 0
    shift = global_shift
    
    ts = np.random.random() * batch_size / txps
    time.sleep(ts)

    t0 = time.time()
    
    while True:
        tx_list = []
        for i in range(batch_size):
            tx_list.append(create_one_tx(i, shift, expire_period))
        send_tx_list(tx_list)
        print("Worker", worker, "sent ", batch_size, "transactions")
        
        n += batch_size
        
        t = time.time()
        if t < t0 + n / txps:
            time.sleep(t0 + n / txps - t)
            
        if expire_period < get_current_period() + 8:
            expire_period = get_current_period() + 8
            shift = global_shift
        else:        
            shift += batch_size


def bench(txps, global_shift):
    global_shift = global_shift * 200000
    workers = 20
    with Pool(workers) as p:
        p.map(send_thread, [(i, txps/workers, global_shift + 10000*i) for i in range(workers)])


if __name__ == "__main__":
    assert len(sys.argv) == 3
    print("test")
    txps = int(sys.argv[1])
    global_shift = int(sys.argv[2]) # use different small integers (e.g. 1, 2, 3, 4) for different scripts (on same machine or different nodes)
    
    credit_wallet()
    
    bench(txps, global_shift)
